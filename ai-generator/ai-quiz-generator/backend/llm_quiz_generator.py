import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import QuizOutput

# Load environment variables from .env file
load_dotenv()

def generate_quiz_from_text(article_text: str) -> QuizOutput:
    """
    Generates a structured quiz from a given article text using Google's Gemini model.
    """

    # Define the Pydantic parser for structured output
    parser = PydanticOutputParser(pydantic_object=QuizOutput)

    # Define the prompt template
    prompt = PromptTemplate(
        template=(
            "You are an AI that generates educational quizzes from Wikipedia articles.\n"
            "Based on the following text, create a structured JSON output:\n\n"
            "{article_text}\n\n"
            "Return the output in this JSON format:\n{format_instructions}"
        ),
        input_variables=["article_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Initialize the Google Generative AI (Gemini) model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

    # Format the input and call the model
    chain_input = prompt.format_prompt(article_text=article_text)
    result = llm.invoke(chain_input.to_string())

    # Parse the structured output into a QuizOutput Pydantic object
    return parser.parse(result.content)
