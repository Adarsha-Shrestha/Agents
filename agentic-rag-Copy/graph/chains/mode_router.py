from typing import Literal, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class ModeDetection(BaseModel):
    """Detect the intended mode from user input"""
    
    mode: Literal["qna", "quiz", "flashcard"] = Field(
        description="Detected mode: 'qna' for question-answering, 'quiz' for quiz generation, 'flashcard' for flashcard generation"
    )
    
    subject: Optional[str] = Field(
        None,
        description="Extract the subject from the input. Should be one of: 'DataMining', 'Network', or None if not specified."
    )
    
    topic: str = Field(
        description="Main topic or theme extracted from the input"
    )
    
    confidence: float = Field(
        description="Confidence score (0.0 to 1.0) for the mode detection"
    )


class RouteWithMode(BaseModel):
    """Route query with mode and subject detection"""

    datasource: Literal["vectorstore", "websearch"] = Field(
        description="Data source to route to"
    )
    
    mode: Literal["qna", "quiz", "flashcard"] = Field(
        description="Operation mode detected"
    )
    
    subject: Optional[str] = Field(
        None,
        description="Subject area if detected"
    )


llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")
mode_detector = llm.with_structured_output(ModeDetection)
mode_router = llm.with_structured_output(RouteWithMode)

mode_detection_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at detecting user intent for educational activities.

Analyze the user input and determine which mode they want:

1. **QNA Mode**: User wants to ask questions and get answers
   - Keywords: "what is", "explain", "how does", "tell me about", "define"
   - Examples: "What is data mining?", "Explain clustering algorithms"

2. **Quiz Mode**: User wants to generate or take a quiz
   - Keywords: "quiz", "test", "questions", "assess", "evaluate", "check my knowledge"
   - Examples: "Create a quiz on data mining", "Test me on network protocols", "Generate questions about clustering"

3. **Flashcard Mode**: User wants to generate flashcards for study
   - Keywords: "flashcards", "study cards", "review", "memorize", "study session"
   - Examples: "Make flashcards for network security", "Create study cards on algorithms", "Generate review cards"

Also extract:
- Subject: DataMining, Network, or None
- Main topic from the input
- Confidence in your detection (0.0-1.0)"""),
    ("human", "{input}")
])

routing_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at routing educational requests to appropriate data sources and determining the operation mode.

Available subjects in vectorstore:
- DataMining: data mining, machine learning, algorithms, clustering, classification, data analysis
- Network: computer networks, network security, protocols, network architecture

Routing rules:
1. If the request is about DataMining or Network subjects → vectorstore
2. For all other topics → websearch

Mode detection:
1. QNA: Direct questions seeking answers/explanations
2. Quiz: Requests to generate or take quizzes/tests
3. Flashcard: Requests to create study materials/flashcards

Examples:
- "What is clustering?" → vectorstore, qna, DataMining
- "Create a quiz on network protocols" → vectorstore, quiz, Network  
- "Make flashcards for data mining" → vectorstore, flashcard, DataMining
- "What's the weather today?" → websearch, qna, None"""),
    ("human", "{input}")
])

def detect_mode_and_subject(user_input: str) -> ModeDetection:
    """Detect mode and subject from user input"""
    return mode_detector.invoke({"input": user_input})

def route_with_mode_detection(user_input: str) -> RouteWithMode:
    """Route request with full mode and subject detection"""
    return mode_router.invoke({"input": user_input})