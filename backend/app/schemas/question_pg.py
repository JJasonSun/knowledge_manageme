from typing import List, Optional, Any, Dict
from pydantic import BaseModel, UUID4, Field
from datetime import datetime

class SkillCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    display_order: Optional[int] = None

class SkillCategoryResponse(SkillCategoryBase):
    id: UUID4

    class Config:
        orm_mode = True

class ExerciseTypeBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    display_order: Optional[int] = None

class ExerciseTypeResponse(ExerciseTypeBase):
    id: UUID4
    skill_category_id: Optional[UUID4] = None
    skill_category: Optional[SkillCategoryResponse] = None

    class Config:
        orm_mode = True

class MediaAssetBase(BaseModel):
    file_url: str
    file_type: Optional[str] = None
    mime_type: Optional[str] = None
    description: Optional[str] = None

class MediaAssetResponse(MediaAssetBase):
    id: UUID4
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ExerciseMediaAssetResponse(BaseModel):
    media_asset: MediaAssetResponse
    usage_role: Optional[str] = None

    class Config:
        orm_mode = True

class ExerciseBase(BaseModel):
    prompt: Optional[str] = None
    exercise_metadata: Optional[Dict[str, Any]] = Field(None, serialization_alias="metadata")
    difficulty_level: Optional[int] = 1
    quality_status: Optional[int] = 0

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class ExerciseResponse(ExerciseBase):
    id: UUID4
    parent_exercise_id: Optional[UUID4] = None
    exercise_type_id: Optional[UUID4] = None
    word_id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    exercise_type: Optional[ExerciseTypeResponse] = None
    media_assets: List[ExerciseMediaAssetResponse] = []
    sub_exercises: List["ExerciseResponse"] = []

    class Config:
        orm_mode = True

class ExerciseListResponse(BaseModel):
    items: List[ExerciseResponse]
    total: int
    page: int
    size: int
    pages: int

ExerciseResponse.update_forward_refs()
