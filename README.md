# AI Wiki Quiz Generator

A full-stack application that transforms Wikipedia articles into structured, educational quizzes using AI (Gemini via LangChain).

## Features

### Core Features
- **Wikipedia Article Scraping**: Automatically extracts content from Wikipedia articles
- **AI-Powered Quiz Generation**: Uses Google's Gemini AI to generate 5-10 questions per article
- **Database Storage**: Persists all generated quizzes in MySQL or PostgreSQL
- **Interactive UI**: Clean, modern React interface with Tailwind CSS
- **Quiz History**: View and revisit all previously generated quizzes

### Enhanced Features
- **Difficulty Levels**: Questions are categorized as easy, medium, or hard
- **Key Entities Extraction**: Automatically identifies people, organizations, and locations
- **Section Grouping**: Questions are organized by article sections
- **Related Topics**: Suggests related Wikipedia articles for further reading
- **Take Quiz Mode**: Interactive quiz mode with scoring and answer validation
- **URL Validation**: Real-time URL validation with article preview
- **Caching**: Prevents duplicate scraping of the same URL
- **Raw HTML Storage**: Stores original HTML for reference

## Project Structure

```
ai-quiz-generator/
├── backend/
│   ├── venv/                       # Python Virtual Environment
│   ├── database.py                 # SQLAlchemy setup and Quiz model
│   ├── models.py                   # Pydantic Schemas for LLM output (QuizOutput)
│   ├── scraper.py                  # Functions for fetching and cleaning Wikipedia HTML
│   ├── llm_quiz_generator.py       # LangChain setup, prompt templates, and chain logic
│   ├── main.py                     # FastAPI application and API endpoints
│   ├── requirements.txt            # List of all Python dependencies
│   └── .env                        # API keys and environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable UI parts (e.g., QuizCard, TabButton, Modal)
│   │   │   ├── QuizDisplay.jsx     # Reusable component for rendering generated quiz data
│   │   │   ├── HistoryTable.jsx    # Table component for quiz history
│   │   │   └── Modal.jsx           # Modal component for quiz details
│   │   ├── services/
│   │   │   └── api.js              # Functions for communicating with the FastAPI backend
│   │   ├── tabs/
│   │   │   ├── GenerateQuizTab.jsx # Tab for generating new quizzes
│   │   │   └── HistoryTab.jsx      # Tab for viewing quiz history
│   │   ├── App.jsx                 # Main React component, handles tab switching
│   │   └── index.css               # Tailwind directives and custom styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md                       # Project Setup, Endpoints, and Testing Instructions
```

## Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 16+** and **npm/yarn** (for frontend)
- **MySQL or PostgreSQL** database
- **Gemini API Key** (free tier available at [Google AI Studio](https://makersuite.google.com/app/apikey))

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your configuration:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     DATABASE_URL=postgresql://user:password@localhost/quiz_generator
     ```
   
   **For MySQL:**
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost/quiz_generator
   ```

6. **Create database:**
   - **PostgreSQL:**
     ```sql
     CREATE DATABASE quiz_generator;
     ```
   - **MySQL:**
     ```sql
     CREATE DATABASE quiz_generator;
     ```

7. **Run the backend server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## API Endpoints

### 1. Validate URL
- **Endpoint:** `GET /validate_url?url={url}`
- **Response:** Returns validation result with article title
- **Example:**
  ```bash
  curl "http://localhost:8000/validate_url?url=https://en.wikipedia.org/wiki/Alan_Turing"
  ```

### 2. Generate Quiz
- **Endpoint:** `POST /generate_quiz`
- **Request Body:**
  ```json
  {
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)"
  }
  ```
- **Response:** Returns the generated quiz in JSON format with:
  - Quiz title and summary
  - Key entities (people, organizations, locations)
  - Article sections
  - Questions with difficulty levels, options, explanations, and section assignments
  - Related topics for further reading
- **Features:**
  - Automatic caching (returns existing quiz if URL already processed)
  - Stores raw HTML in database
- **Example:**
  ```bash
  curl -X POST "http://localhost:8000/generate_quiz" \
       -H "Content-Type: application/json" \
       -d '{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}'
  ```

### 3. Get Quiz History
- **Endpoint:** `GET /history`
- **Response:** Returns a list of all generated quizzes with `id`, `url`, `title`, and `date_generated`
- **Example:**
  ```bash
  curl "http://localhost:8000/history"
  ```

### 4. Get Quiz by ID
- **Endpoint:** `GET /quiz/{quiz_id}`
- **Response:** Returns the full quiz data for the specified ID
- **Example:**
  ```bash
  curl "http://localhost:8000/quiz/1"
  ```

## Usage

1. **Generate a Quiz:**
   - Navigate to the "Generate Quiz" tab
   - Enter a Wikipedia article URL (e.g., `https://en.wikipedia.org/wiki/Artificial_intelligence`)
   - The system will automatically validate the URL and show the article title
   - Click "Generate Quiz"
   - Wait for the AI to process the article and generate questions
   - View the generated quiz with:
     - Questions organized by section (if available)
     - Difficulty levels (easy, medium, hard)
     - Key entities (people, organizations, locations)
     - Related topics for further reading
   - Toggle "Take Quiz" mode to test your knowledge with scoring

2. **View History:**
   - Navigate to the "History" tab
   - See a table of all previously generated quizzes
   - Click "Details" on any quiz to view it in a modal
   - Use "Take Quiz" mode in the modal to take the quiz again

### Take Quiz Mode
- Click the "Take Quiz" button to hide answers
- Select your answers for each question
- Click "Submit Quiz" to see your score
- View explanations for each question
- Toggle back to "View Answers" to see all correct answers

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for LLM application development
- **Google Gemini**: Large Language Model for quiz generation
- **SQLAlchemy**: SQL toolkit and ORM
- **BeautifulSoup4**: HTML parsing and web scraping
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: JavaScript library for building user interfaces
- **Vite**: Next-generation frontend build tool
- **Tailwind CSS**: Utility-first CSS framework

### Database
- **MySQL** or **PostgreSQL**: Relational database for data persistence

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Ensure your database is running
   - Verify the `DATABASE_URL` in `.env` is correct
   - Check that the database exists

2. **Gemini API Key Error:**
   - Verify your API key is set in `.env`
   - Check that the API key is valid and has quota available

3. **CORS Errors:**
   - Ensure the frontend is running on the ports specified in `main.py` (5173 or 3000)
   - Check that CORS middleware is properly configured

4. **Wikipedia Scraping Issues:**
   - Verify the URL is a valid Wikipedia article
   - Check your internet connection
   - Some articles may have restricted access

## Development

### Running Tests
- Backend: Use FastAPI's built-in test client or pytest
- Frontend: Use React Testing Library or similar

### Code Style
- Backend: Follow PEP 8 Python style guide
- Frontend: Use ESLint and Prettier for code formatting

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# ai-quiz-generator
