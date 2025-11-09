from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    options: List[str]
    answer: str

class QuizOutput(BaseModel):
    title: str
    summary: str
    questions: List[Question]
