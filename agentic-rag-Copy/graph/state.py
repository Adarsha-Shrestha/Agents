from typing import List, TypedDict, Optional


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        subject: subject filter for retrieval
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
        sources: source information from document metadata
    """

    question: str
    subject: Optional[str]  # Added subject field
    generation: str
    web_search: bool
    documents: List[str]
    sources: Optional[List[dict]]  # Added sources field
    mode: str  # qna, quiz, or flashcard
    quiz_data: Optional[List[dict[str, any]]]
    flashcard_data: Optional[List[dict[str, str]]]
    quiz_config: Optional[dict[str, any]]
    flashcard_config: Optional[dict[str, any]]