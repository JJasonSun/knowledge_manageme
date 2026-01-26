from typing import List, Optional, Any, Dict
from pydantic import BaseModel, UUID4, Field
from datetime import datetime

class SLSkillCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    display_order: Optional[int] = None

class SLSkillCategoryResponse(SLSkillCategoryBase):
    id: UUID4

    class Config:
        orm_mode = True

class SLExerciseTypeBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    display_order: Optional[int] = None

class SLExerciseTypeResponse(SLExerciseTypeBase):
    id: UUID4
    skill_category_id: Optional[UUID4] = None

    class Config:
        orm_mode = True

class SLMediaAssetBase(BaseModel):
    file_url: str
    file_type: Optional[str] = None
    mime_type: Optional[str] = None
    description: Optional[str] = None

class SLMediaAssetResponse(SLMediaAssetBase):
    id: UUID4
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class SLExerciseMediaAssetResponse(BaseModel):
    media_asset: SLMediaAssetResponse
    usage_role: Optional[str] = None

    class Config:
        orm_mode = True

class SLExerciseBase(BaseModel):
    prompt: Optional[str] = None
    exercise_metadata: Optional[Dict[str, Any]] = Field(None, serialization_alias="metadata")
    difficulty_level: Optional[int] = 1
    display_order: Optional[int] = None
    
    # Specific fields
    vocab_package_db_id: Optional[int] = None
    source_lesson_db_id: Optional[int] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class SLExerciseResponse(SLExerciseBase):
    id: UUID4
    parent_exercise_id: Optional[UUID4] = None
    exercise_type_id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    exercise_type: Optional[SLExerciseTypeResponse] = None
    media_assets: List[SLExerciseMediaAssetResponse] = []
    sub_exercises: List["SLExerciseResponse"] = []

    class Config:
        orm_mode = True

class SLExerciseListResponse(BaseModel):
    items: List[SLExerciseResponse]
    total: int
    page: int
    size: int
    pages: int

SLExerciseResponse.update_forward_refs()
