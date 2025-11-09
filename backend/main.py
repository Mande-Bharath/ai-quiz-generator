# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, SessionLocal
from models import QuizRecord, GeneratedQuiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz
from sqlalchemy.orm import Session
import json

app = FastAPI(title="AI Quiz Generator")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
async def startup_event():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Quiz Generator API"}

@app.post("/generate_quiz")
async def create_quiz(url: str, db: Session = Depends(get_db)):
    try:
        # Scrape Wikipedia article
        article = scrape_wikipedia(url)
        
        # Generate quiz using LLM
        quiz_data = generate_quiz(article)
        
        # Store in database
        db_quiz = QuizRecord(
            url=quiz_data.get("url") or url,
            title=quiz_data.get("title") or article.get("title"),
            scraped_text=article.get("text"),
            full_quiz_data=json.dumps(quiz_data)
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        
        return quiz_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    quizzes = db.query(QuizRecord).order_by(QuizRecord.date_generated.desc()).all()
    return [{
        "id": q.id,
        "url": q.url,
        "title": q.title,
        "date_generated": q.date_generated
    } for q in quizzes]

@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    try:
        return json.loads(quiz.full_quiz_data)
    except Exception:
        return {"id": quiz.id, "url": quiz.url, "title": quiz.title, "full_quiz_data": quiz.full_quiz_data}

# Add cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    # nothing to cleanup here (sessions are closed by dependency)
    return
