from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from typing import Optional, List, Union
from uuid import UUID

from app.core.database import get_questions_db
from app.models.question_pg import Exercise
from app.models.scenario_pg import SLExercise
from app.schemas.question_pg import ExerciseResponse, ExerciseListResponse
from app.schemas.scenario_pg import SLExerciseResponse, SLExerciseListResponse

router = APIRouter()

@router.get("/questions", response_model=Union[ExerciseListResponse, SLExerciseListResponse])
async def get_questions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    type_id: Optional[UUID] = None,
    difficulty: Optional[int] = None,
    search: Optional[str] = None,
    source: str = Query("content_system", enum=["content_system", "scenario_system"]),
    db: Session = Depends(get_questions_db)
):
    """
    获取题目列表 (PostgreSQL)
    只读接口，严禁修改数据
    
    - **source**: 题目来源，可选 "content_system" (默认) 或 "scenario_system"
    - **search**: 搜索关键词 (匹配题目内容或元数据)
    """
    try:
        if source == "content_system":
            # 只查询父题目（非子题）
            query = db.query(Exercise).filter(Exercise.parent_exercise_id == None)
            
            if type_id:
                query = query.filter(Exercise.exercise_type_id == type_id)
            
            if difficulty:
                query = query.filter(Exercise.difficulty_level == difficulty)
                
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        Exercise.prompt.ilike(search_term),
                        cast(Exercise.exercise_metadata, String).ilike(search_term)
                    )
                )
                
            total = query.count()
            
            offset = (page - 1) * size
            exercises = query.offset(offset).limit(size).all()
            
            return {
                "items": exercises,
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size
            }
        else:
            # Scenario Learning System
            query = db.query(SLExercise).filter(SLExercise.parent_exercise_id == None)
            
            if type_id:
                query = query.filter(SLExercise.exercise_type_id == type_id)
            
            if difficulty:
                query = query.filter(SLExercise.difficulty_level == difficulty)
                
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        SLExercise.prompt.ilike(search_term),
                        cast(SLExercise.exercise_metadata, String).ilike(search_term)
                    )
                )
            
            # Scenario system usually orders by display_order
            query = query.order_by(SLExercise.display_order)

            total = query.count()
            
            offset = (page - 1) * size
            exercises = query.offset(offset).limit(size).all()
            
            return {
                "items": exercises,
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取题目失败: {str(e)}")

@router.get("/questions/{question_id}", response_model=Union[ExerciseResponse, SLExerciseResponse])
async def get_question(
    question_id: UUID,
    source: Optional[str] = Query(None, enum=["content_system", "scenario_system"]),
    db: Session = Depends(get_questions_db)
):
    """
    获取单个题目详情 (PostgreSQL)
    如果不指定 source，将依次查找 content_system 和 scenario_system
    """
    try:
        exercise = None
        
        # 1. Try content_system if source is None or specified
        if source == "content_system" or source is None:
            exercise = db.query(Exercise).filter(Exercise.id == question_id).first()
            if exercise and source is None:
                # Found in content_system
                return exercise
            elif exercise:
                return exercise

        # 2. Try scenario_system if source is None or specified
        if source == "scenario_system" or (source is None and exercise is None):
            sl_exercise = db.query(SLExercise).filter(SLExercise.id == question_id).first()
            if sl_exercise:
                return sl_exercise
        
        if not exercise and (source == "scenario_system" or source is None):
             # If we reached here and exercise is still None (and we tried scenario), then not found
             raise HTTPException(status_code=404, detail="题目不存在")

        # Handle case where source was content_system but not found
        if source == "content_system" and not exercise:
            raise HTTPException(status_code=404, detail="题目不存在")
            
        return exercise # Should be caught by logic above, but for safety

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取题目详情失败: {str(e)}")
