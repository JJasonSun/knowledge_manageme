from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import BasePG

class SLSkillCategory(BasePG):
    __tablename__ = "sl_skill_categories"
    __table_args__ = {"schema": "scenario_learning_v2"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    display_order = Column(Integer, unique=True)

class SLExerciseType(BasePG):
    __tablename__ = "sl_exercise_types"
    __table_args__ = {"schema": "scenario_learning_v2"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_category_id = Column(UUID(as_uuid=True), ForeignKey("scenario_learning_v2.sl_skill_categories.id"))
    name = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255))
    description = Column(Text)
    display_order = Column(Integer)

    skill_category = relationship("SLSkillCategory")

class GeneratedLesson(BasePG):
    __tablename__ = "generated_lessons"
    __table_args__ = {"schema": "scenario_learning_v2"}

    lesson_db_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer)
    lesson_name = Column(String(255))
    type = Column(String(50))
    passage = Column(JSONB)
    lesson_id_str = Column(String(255))
    generated_at = Column(DateTime(timezone=True))

class Vocabulary(BasePG):
    __tablename__ = "vocabulary"
    __table_args__ = {"schema": "scenario_learning_v2"}

    vocab_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word = Column(String(255))
    hsk_level = Column(Integer)

class GeneratedVocabPackage(BasePG):
    __tablename__ = "generated_vocab_packages"
    __table_args__ = {"schema": "scenario_learning_v2"}

    vocab_package_db_id = Column(Integer, primary_key=True)
    lesson_db_id = Column(Integer, ForeignKey("scenario_learning_v2.generated_lessons.lesson_db_id"))
    vocab_uuid = Column(UUID(as_uuid=True), ForeignKey("scenario_learning_v2.vocabulary.vocab_uuid"))

    lesson = relationship("GeneratedLesson")
    vocab = relationship("Vocabulary")

class SLMediaAsset(BasePG):
    __tablename__ = "sl_media_assets"
    __table_args__ = {"schema": "scenario_learning_v2"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_url = Column(Text, unique=True)
    file_type = Column(String(50))
    mime_type = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class SLExercise(BasePG):
    __tablename__ = "sl_exercises"
    __table_args__ = {"schema": "scenario_learning_v2"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_exercise_id = Column(UUID(as_uuid=True), ForeignKey("scenario_learning_v2.sl_exercises.id"), nullable=True)
    exercise_type_id = Column(UUID(as_uuid=True), ForeignKey("scenario_learning_v2.sl_exercise_types.id"))
    
    # Specific fields for scenario learning
    vocab_package_db_id = Column(Integer, ForeignKey("scenario_learning_v2.generated_vocab_packages.vocab_package_db_id"), nullable=True)
    source_lesson_db_id = Column(Integer, ForeignKey("scenario_learning_v2.generated_lessons.lesson_db_id"), nullable=True)
    
    prompt = Column(Text)
    exercise_metadata = Column("metadata", JSONB)
    difficulty_level = Column(SmallInteger, default=1)
    display_order = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    exercise_type = relationship("SLExerciseType")
    source_lesson = relationship("GeneratedLesson", foreign_keys=[source_lesson_db_id])
    vocab_package = relationship("GeneratedVocabPackage", foreign_keys=[vocab_package_db_id])
    parent_exercise = relationship("SLExercise", remote_side=[id], backref="sub_exercises")
    media_assets = relationship("SLExerciseMediaAsset", back_populates="exercise")

class SLExerciseMediaAsset(BasePG):
    __tablename__ = "sl_exercise_media_assets"
    __table_args__ = {"schema": "scenario_learning_v2"}

    exercise_id = Column(UUID(as_uuid=True), ForeignKey("scenario_learning_v2.sl_exercises.id"), primary_key=True)
    media_asset_id = Column(UUID(as_uuid=True), ForeignKey("scenario_learning_v2.sl_media_assets.id"), primary_key=True)
    usage_role = Column(String(100))

    exercise = relationship("SLExercise", back_populates="media_assets")
    media_asset = relationship("SLMediaAsset")
