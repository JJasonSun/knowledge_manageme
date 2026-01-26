from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime, Boolean, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import BasePG

class SkillCategory(BasePG):
    __tablename__ = "skill_categories"
    __table_args__ = {"schema": "content_new"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    display_order = Column(Integer, unique=True)

class ExerciseType(BasePG):
    __tablename__ = "exercise_types"
    __table_args__ = {"schema": "content_new"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_category_id = Column(UUID(as_uuid=True), ForeignKey("content_new.skill_categories.id"))
    name = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255))
    description = Column(Text)
    display_order = Column(Integer)

    skill_category = relationship("SkillCategory")

class MediaAsset(BasePG):
    __tablename__ = "media_assets"
    __table_args__ = {"schema": "content_new"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_url = Column(Text, unique=True)
    file_type = Column(String(50))
    mime_type = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class Word(BasePG):
    __tablename__ = "words"
    __table_args__ = {"schema": "content_new"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    characters = Column(String(100), unique=True, nullable=False)
    pinyin = Column(String(255))
    translation = Column(Text)
    hsk_level = Column(SmallInteger)
    audio_url = Column(Text)

class Exercise(BasePG):
    __tablename__ = "exercises"
    __table_args__ = {"schema": "content_new"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_exercise_id = Column(UUID(as_uuid=True), ForeignKey("content_new.exercises.id"), nullable=True)
    exercise_type_id = Column(UUID(as_uuid=True), ForeignKey("content_new.exercise_types.id"))
    word_id = Column(UUID(as_uuid=True), ForeignKey("content_new.words.id"), nullable=True)
    prompt = Column(Text)
    exercise_metadata = Column("metadata", JSONB)
    difficulty_level = Column(SmallInteger, default=1)
    quality_status = Column(SmallInteger, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    exercise_type = relationship("ExerciseType")
    word = relationship("Word")
    parent_exercise = relationship("Exercise", remote_side=[id], backref="sub_exercises")
    media_assets = relationship("ExerciseMediaAsset", back_populates="exercise")

class ExerciseMediaAsset(BasePG):
    __tablename__ = "exercise_media_assets"
    __table_args__ = {"schema": "content_new"}

    exercise_id = Column(UUID(as_uuid=True), ForeignKey("content_new.exercises.id"), primary_key=True)
    media_asset_id = Column(UUID(as_uuid=True), ForeignKey("content_new.media_assets.id"), primary_key=True)
    usage_role = Column(String(100))

    exercise = relationship("Exercise", back_populates="media_assets")
    media_asset = relationship("MediaAsset")
