"""
中文教育资源管理系统 - FastAPI应用入口
"""
from fastapi import FastAPI, HTTPException, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import logging

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db, test_connection, ensure_owner_columns
from app.core.simple_auth import authenticate_user, create_access_token, verify_token, get_current_user
from app.models.chengyu import Chengyu
from app.models.ciyu import Ciyu
from app.schemas.chengyu import ChengyuResponse, ChengyuListResponse, ChengyuCreate, ChengyuUpdate
from app.schemas.ciyu import CiyuResponse, CiyuListResponse, CiyuCreate, CiyuUpdate
from app.schemas.common import APIResponse, PaginatedResponse, SearchParams
from app.schemas.user import UserLogin, UserResponse, Token

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="中文教育资源管理系统 API",
    version=settings.VERSION,
    debug=settings.DEBUG,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP Bearer认证
security = HTTPBearer()


def ensure_owner_or_admin(resource, current_user):
    owner = getattr(resource, "created_by", None)
    if current_user.role == "admin":
        return
    if owner and owner == current_user.username:
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")

# 根路径
@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "中文教育资源管理系统 API",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "running"
    }

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}

# 认证相关接口
@app.post("/api/v1/auth/login", response_model=Token)
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """用户登录接口"""
    logger.info(f"用户登录尝试: {username}")
    
    # 验证用户
    user = authenticate_user(username, password)
    if not user:
        logger.warning(f"登录失败: 用户名或密码错误 - {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token = create_access_token(username=user.username, role=user.role)
    logger.info(f"用户登录成功: {user.username}, 角色: {user.role}")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            role=user.role
        )
    )

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role
    )

# 成语相关接口
@app.get("/api/v1/chengyu", response_model=ChengyuListResponse)
async def get_chengyu_list(
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取成语列表"""
    try:
        query = db.query(Chengyu)
        
        # 搜索过滤
        if search:
            query = query.filter(
                or_(
                    Chengyu.chengyu.like(f"%{search}%"),
                    Chengyu.pinyin.like(f"%{search}%"),
                    Chengyu.explanation.like(f"%{search}%")
                )
            )
        
        # 分页
        total = query.count()
        offset = (page - 1) * size
        chengyu_list = query.order_by(Chengyu.created_at.desc()).offset(offset).limit(size).all()
        
        return ChengyuListResponse(
            items=[ChengyuResponse.from_orm(chengyu) for chengyu in chengyu_list],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    except Exception as e:
        logger.error(f"获取成语列表失败: {str(e)}")
        import traceback
        logger.error(f"详细错误: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"获取成语列表失败: {str(e)}")

@app.get("/api/v1/chengyu/{chengyu_id}", response_model=ChengyuResponse)
async def get_chengyu(chengyu_id: int, db: Session = Depends(get_db)):
    """获取单个成语详情"""
    chengyu = db.query(Chengyu).filter(Chengyu.id == chengyu_id).first()
    if not chengyu:
        raise HTTPException(status_code=404, detail="成语不存在")
    return ChengyuResponse.from_orm(chengyu)

@app.post("/api/v1/chengyu", response_model=ChengyuResponse)
async def create_chengyu(
    chengyu_data: ChengyuCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新成语（仅管理员和老师）"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        chengyu = Chengyu(**chengyu_data.dict(), created_by=current_user.username)
        db.add(chengyu)
        db.commit()
        db.refresh(chengyu)
        logger.info(f"用户 {current_user.username} 创建了成语: {chengyu.chengyu}")
        return ChengyuResponse.from_orm(chengyu)
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        logger.error(f"创建成语失败: {error_msg}")
        
        # 检查是否是重复错误
        if "Duplicate entry" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="该成语已存在"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="创建成语失败"
            )


@app.put("/api/v1/chengyu/{chengyu_id}", response_model=ChengyuResponse)
async def update_chengyu(
    chengyu_id: int,
    chengyu_data: ChengyuUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chengyu = db.query(Chengyu).filter(Chengyu.id == chengyu_id).first()
    if not chengyu:
        raise HTTPException(status_code=404, detail="成语不存在")

    ensure_owner_or_admin(chengyu, current_user)

    payload = chengyu_data.dict(exclude_unset=True)
    if not payload:
        raise HTTPException(status_code=400, detail="没有更新字段")

    try:
        for key, value in payload.items():
            setattr(chengyu, key, value)
        db.commit()
        db.refresh(chengyu)
        logger.info(f"用户 {current_user.username} 更新了成语: {chengyu.chengyu}")
        return ChengyuResponse.from_orm(chengyu)
    except Exception as e:
        db.rollback()
        logger.error(f"更新成语失败: {e}")
        raise HTTPException(status_code=500, detail="更新成语失败")


@app.delete("/api/v1/chengyu/{chengyu_id}")
async def delete_chengyu(
    chengyu_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chengyu = db.query(Chengyu).filter(Chengyu.id == chengyu_id).first()
    if not chengyu:
        raise HTTPException(status_code=404, detail="成语不存在")

    ensure_owner_or_admin(chengyu, current_user)

    try:
        db.delete(chengyu)
        db.commit()
        logger.info(f"用户 {current_user.username} 删除了成语: {chengyu.chengyu}")
        return APIResponse(success=True, message="成语已删除")
    except Exception as e:
        db.rollback()
        logger.error(f"删除成语失败: {e}")
        raise HTTPException(status_code=500, detail="删除成语失败")

# 词语相关接口
@app.get("/api/v2/ciyu", response_model=CiyuListResponse)
async def get_ciyu_list(
    page: int = 1,
    size: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取词语列表"""
    try:
        query = db.query(Ciyu)
        
        # 搜索过滤
        if search:
            query = query.filter(
                or_(
                    Ciyu.word.like(f"%{search}%"),
                    Ciyu.pinyin.like(f"%{search}%"),
                    Ciyu.definition.like(f"%{search}%")
                )
            )
        
        # 分页
        total = query.count()
        offset = (page - 1) * size
        ciyu_list = query.order_by(Ciyu.created_at.desc()).offset(offset).limit(size).all()
        
        return CiyuListResponse(
            items=[CiyuResponse.from_orm(ciyu) for ciyu in ciyu_list],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    except Exception as e:
        logger.error(f"获取词语列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取词语列表失败")

@app.get("/api/v2/ciyu/{ciyu_id}", response_model=CiyuResponse)
async def get_ciyu(ciyu_id: int, db: Session = Depends(get_db)):
    """获取单个词语详情"""
    ciyu = db.query(Ciyu).filter(Ciyu.id == ciyu_id).first()
    if not ciyu:
        raise HTTPException(status_code=404, detail="词语不存在")
    return CiyuResponse.from_orm(ciyu)

@app.post("/api/v2/ciyu", response_model=CiyuResponse)
async def create_ciyu(
    ciyu_data: CiyuCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新词语（仅管理员和老师）"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        ciyu = Ciyu(**ciyu_data.dict(), created_by=current_user.username)
        db.add(ciyu)
        db.commit()
        db.refresh(ciyu)
        logger.info(f"用户 {current_user.username} 创建了词语: {ciyu.word}")
        return CiyuResponse.from_orm(ciyu)
    except Exception as e:
        db.rollback()
        logger.error(f"创建词语失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建词语失败")


@app.put("/api/v2/ciyu/{ciyu_id}", response_model=CiyuResponse)
async def update_ciyu(
    ciyu_id: int,
    ciyu_data: CiyuUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ciyu = db.query(Ciyu).filter(Ciyu.id == ciyu_id).first()
    if not ciyu:
        raise HTTPException(status_code=404, detail="词语不存在")

    ensure_owner_or_admin(ciyu, current_user)

    payload = ciyu_data.dict(exclude_unset=True)
    if not payload:
        raise HTTPException(status_code=400, detail="没有更新字段")

    try:
        for key, value in payload.items():
            setattr(ciyu, key, value)
        db.commit()
        db.refresh(ciyu)
        logger.info(f"用户 {current_user.username} 更新了词语: {ciyu.word}")
        return CiyuResponse.from_orm(ciyu)
    except Exception as e:
        db.rollback()
        logger.error(f"更新词语失败: {e}")
        raise HTTPException(status_code=500, detail="更新词语失败")


@app.delete("/api/v2/ciyu/{ciyu_id}")
async def delete_ciyu(
    ciyu_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ciyu = db.query(Ciyu).filter(Ciyu.id == ciyu_id).first()
    if not ciyu:
        raise HTTPException(status_code=404, detail="词语不存在")

    ensure_owner_or_admin(ciyu, current_user)

    try:
        db.delete(ciyu)
        db.commit()
        logger.info(f"用户 {current_user.username} 删除了词语: {ciyu.word}")
        return APIResponse(success=True, message="词语已删除")
    except Exception as e:
        db.rollback()
        logger.error(f"删除词语失败: {e}")
        raise HTTPException(status_code=500, detail="删除词语失败")

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("正在启动中文教育资源管理系统...")
    
    # 确保 created_by 字段存在
    if ensure_owner_columns():
        print("created_by 字段已准备就绪")
    else:
        print("警告: 无法确保 created_by 字段")

    # 测试数据库连接
    if test_connection():
        print("数据库连接正常")
    else:
        print("警告: 数据库连接失败")
    
    print(f"应用启动完成，访问地址: http://localhost:8000")
    print(f"API文档地址: http://localhost:8000/docs")
    logger.info("中文教育资源管理系统启动")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("中文教育资源管理系统正在关闭...")
    logger.info("中文教育资源管理系统关闭")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    db_status = "connected" if test_connection() else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )