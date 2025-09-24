from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class QueryType(BaseModel):
    """Classify query type"""
    
    is_conversational: bool = Field(
        description="True if this is a simple greeting, casual conversation, or social interaction"
    )
    is_question: bool = Field(
        description="True if this requires factual information or knowledge"
    )


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
structured_llm = llm.with_structured_output(QueryType)

system = """You are an expert at classifying user queries. Determine if a query is:

1. CONVERSATIONAL: Simple greetings (hello, hi, how are you), casual chat, social interactions, or pleasantries
2. QUESTION: Requests for factual information, explanations, or knowledge

Examples:
- "hello" → conversational: true, question: false  
- "hi there" → conversational: true, question: false
- "how are you?" → conversational: true, question: false
- "what is classification?" → conversational: false, question: true
- "explain TCP protocol" → conversational: false, question: true
- "thanks" → conversational: true, question: false

Be strict: only mark as question if it genuinely seeks factual information."""

query_classifier_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "Query: {query}")
])

query_classifier = query_classifier_prompt | structured_llm


def detect_conversational_query(query: str) -> Dict[str, bool]:
    """
    Detect if a query is conversational or informational
    
    Args:
        query: User input query
        
    Returns:
        Dict with is_conversational and is_question flags
    """
    result = query_classifier.invoke({"query": query})
    return {
        "is_conversational": result.is_conversational,
        "is_question": result.is_question
    }