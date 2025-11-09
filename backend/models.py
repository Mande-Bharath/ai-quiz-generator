# models.py
from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QuizRecord(Base):
    __tablename__ = "quiz_records"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1024), nullable=False)
    title = Column(String(512))
    scraped_text = Column(Text)            # raw text from article
    full_quiz_data = Column(Text, nullable=False)  # JSON string
    date_generated = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic models for validation / LLM output enforcement

class QuizQuestion(BaseModel):
    id: int
    question: str
    type: str  # "multiple_choice" or "short_answer"
    options: List[str] = []
    correct_answers: List[int] = []
    explanation: Optional[str] = None

class GeneratedQuiz(BaseModel):
    title: str
    url: str
    summary: str
    difficulty: str
    questions: List[QuizQuestion]
    metadata: Dict[str, Any] = {}
