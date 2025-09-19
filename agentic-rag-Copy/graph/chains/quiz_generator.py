from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class QuizQuestion(BaseModel):
    """Single quiz question with options and answer"""
    question: str = Field(description="The quiz question")
    options: List[str] = Field(description="List of 4 multiple choice options (A, B, C, D)")
    correct_answer: str = Field(description="The correct answer (A, B, C, or D)")
    explanation: str = Field(description="Explanation of why this is the correct answer")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")


class QuizData(BaseModel):
    """Collection of quiz questions"""
    questions: List[QuizQuestion] = Field(description="List of quiz questions")
    topic: str = Field(description="Topic or subject of the quiz")
    total_questions: int = Field(description="Total number of questions generated")


llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
structured_llm_quiz = llm.with_structured_output(QuizData)

quiz_system_prompt = """You are an expert educational content creator specializing in generating high-quality quiz questions from academic material.

Your task is to create multiple-choice quiz questions based on the provided documents. Follow these guidelines:

1. **Question Quality:**
   - Create clear, unambiguous questions
   - Ensure questions test understanding, not just memorization
   - Include a mix of difficulty levels (easy, medium, hard)
   - Cover different aspects of the topic

2. **Options:**
   - Provide exactly 4 options (A, B, C, D)
   - Make sure only one option is clearly correct
   - Create plausible distractors (incorrect options that seem reasonable)
   - Avoid options like "All of the above" or "None of the above"

3. **Content Coverage:**
   - Generate questions that cover the main concepts in the documents
   - Include both factual and conceptual questions
   - Test different cognitive levels (remember, understand, apply, analyze)

4. **Format:**
   - Label options as A, B, C, D
   - Provide clear explanations for correct answers
   - Assign appropriate difficulty levels

Generate {num_questions} questions based on the provided content."""

quiz_prompt = ChatPromptTemplate.from_messages([
    ("system", quiz_system_prompt),
    ("human", """Topic: {topic}
    
Documents:
{documents}

Number of questions to generate: {num_questions}

Please generate quiz questions based on this content.""")
])

quiz_generator: RunnableSequence = quiz_prompt | structured_llm_quiz


def generate_quiz_from_documents(documents, topic="General", num_questions=5, difficulty_mix=None):
    """
    Generate quiz questions from documents
    
    Args:
        documents: List of document objects
        topic: Topic name for the quiz
        num_questions: Number of questions to generate
        difficulty_mix: Dict specifying difficulty distribution
    
    Returns:
        QuizData: Generated quiz data
    """
    if difficulty_mix is None:
        difficulty_mix = {"easy": 2, "medium": 2, "hard": 1}
    
    # Combine document content
    doc_content = "\n\n".join([doc.page_content for doc in documents])
    
    # Generate quiz
    quiz_result = quiz_generator.invoke({
        "documents": doc_content,
        "topic": topic,
        "num_questions": num_questions
    })
    
    return quiz_result