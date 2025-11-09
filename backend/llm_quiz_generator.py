# llm_quiz_generator.py
import os
import re
import random
from dotenv import load_dotenv
from typing import Dict, Optional, List
from pydantic import ValidationError

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Try to import the Google Gemini LLM wrapper; if unavailable we'll fallback
try:
    from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
    LLM_AVAILABLE = True
except Exception:
    ChatGoogleGenerativeAI = None  # type: ignore
    LLM_AVAILABLE = False

from models import GeneratedQuiz, QuizQuestion


def _split_sentences(text: str) -> List[str]:
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if len(s.strip()) > 40]


def _make_cloze_question(sentence: str, qid: int) -> Dict:
    words = re.findall(r"\w{4,}", sentence)
    if not words:
        # fallback: truncate sentence
        question_text = sentence[:120].rstrip() + "..."
        return {
            "id": qid,
            "question": f"Explain: {question_text}",
            "type": "short_answer",
            "options": [],
            "correct_answers": [],
            "explanation": ""
        }
    # pick a keyword to blank out
    keyword = random.choice(words)
    cloze = sentence.replace(keyword, "____", 1)
    return {
        "id": qid,
        "question": cloze,
        "type": "short_answer",
        "options": [],
        "correct_answers": [],
        "explanation": f"Answer was: {keyword}"
    }


def _simple_fallback_quiz(article: Dict) -> Dict:
    text = article.get("text", "")
    sents = _split_sentences(text)
    num_q = min(5, max(1, len(sents)//10 if len(sents) >= 10 else len(sents)))
    chosen = []
    if not sents:
        # minimal fallback
        questions = [{
            "id": 1,
            "question": "Write a short summary of the article.",
            "type": "short_answer",
            "options": [],
            "correct_answers": [],
            "explanation": ""
        }]
    else:
        # pick sentences spaced across the article
        step = max(1, len(sents)//num_q)
        for i in range(0, num_q*step, step):
            if i < len(sents):
                chosen.append(sents[i])
        # ensure uniqueness and cap count
        chosen = chosen[:5]
        questions = [_make_cloze_question(s, idx+1) for idx, s in enumerate(chosen)]

    quiz = {
        "title": article.get("title") or "Untitled",
        "url": article.get("url") or "",
        "summary": (article.get("text", "")[:400] + "...") if article.get("text") else "",
        "difficulty": "medium",
        "questions": questions,
        "metadata": {"generator": "fallback"}
    }
    return quiz


def instantiate_llm():
    if not LLM_AVAILABLE:
        return None
    # instantiate ChatGoogleGenerativeAI if available
    try:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.2
        )
        return llm
    except Exception:
        return None


def generate_quiz(article: Dict) -> Dict:
    """
    Generate a quiz dict for the given article.
    Attempts to use Gemini via langchain_google_genai if present; otherwise uses a safe fallback.
    The returned dict conforms to the GeneratedQuiz Pydantic schema.
    """
    # If LLM is available, attempt to call it (best-effort). If anything fails, use fallback.
    llm = instantiate_llm()
    if llm is not None:
        try:
            # best-effort prompt + LLM call; library wrappers differ between versions,
            # so we attempt common call styles and fall back on the simple generator.
            prompt = (
                f"Given the following article text, produce a JSON object matching "
                f"the schema: {{'title':str,'url':str,'summary':str,'difficulty':str,'questions':[]}}. "
                f"Include 4-6 questions (each with id, question, type, options, correct_answers, explanation).\n\n"
                f"Article:\n\n{article.get('text','')[:4000]}"
            )
            # try common method names
            if hasattr(llm, "generate"):
                resp = llm.generate(prompt)
                text = getattr(resp, "text", None) or str(resp)
            elif hasattr(llm, "predict"):
                text = llm.predict(prompt)
            else:
                # last resort: call str()
                text = str(llm.__class__)  # not useful, will fallback next
            # try to parse JSON from the LLM text
            import json, re
            m = re.search(r"(\{.*\})", text, re.S)
            if m:
                obj = json.loads(m.group(1))
                # validate
                quiz = GeneratedQuiz(**obj)
                return quiz.dict()
        except Exception:
            pass

    # fallback generator (safe)
    fallback = _simple_fallback_quiz(article)
    try:
        quiz = GeneratedQuiz(**fallback)
        return quiz.dict()
    except ValidationError as e:
        # last-resort minimal valid structure
        minimal = {
            "title": article.get("title") or "Untitled",
            "url": article.get("url") or "",
            "summary": article.get("text","")[:200],
            "difficulty": "medium",
            "questions": [],
            "metadata": {"error": str(e)}
        }
        return minimal
