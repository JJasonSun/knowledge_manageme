from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import test_connection

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="中文教育资源管理系统API",
    debug=settings.DEBUG,
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    """
    print("正在启动中文教育资源管理系统...")
    
    # 测试数据库连接
    if test_connection():
        print("数据库连接正常")
    else:
        print("警告: 数据库连接失败")
    
    print(f"应用启动完成，访问地址: http://localhost:8000")
    print(f"API文档地址: http://localhost:8000/docs")


@app.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": "欢迎使用中文教育资源管理系统",
        "version": settings.VERSION,
        "status": "running"
    }


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