from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz_from_text
from database import Quiz, SessionLocal, init_db
from sqlalchemy.orm import Session
import json

# Initialize FastAPI app
app = FastAPI(title="AI Quiz Generator Backend", version="1.0")

# Allow CORS for frontend
origins = [
    "http://localhost:5173",
    "https://ai-quiz-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db()

# ✅ Root route (health check)
@app.get("/")
def root():
    return {"message": "AI Quiz Generator backend is running 🚀"}


# ✅ Generate a quiz from a Wikipedia URL
@app.post("/generate_quiz")
def generate_quiz(data: dict):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        # Scrape article content
        article_text = scrape_wikipedia(url)

        # Generate quiz using the LLM
        quiz = generate_quiz_from_text(article_text)

        # Save quiz in database
        db: Session = SessionLocal()
        new_quiz = Quiz(
            url=url,
            title=quiz.title,
            content=article_text[:2000],  # truncate content for storage
            quiz_data=json.dumps(quiz.dict())
        )
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        db.close()

        return quiz.dict()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


# ✅ Get quiz generation history
@app.get("/history")
def get_history():
    db: Session = SessionLocal()
    quizzes = db.query(Quiz).all()
    db.close()
    return [
        {
            "id": q.id,
            "url": q.url,
            "title": q.title,
            "date_generated": q.date_generated
        }
        for q in quizzes
    ]


# ✅ Retrieve a specific quiz by ID
@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int):
    db: Session = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    db.close()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return json.loads(quiz.quiz_data)
