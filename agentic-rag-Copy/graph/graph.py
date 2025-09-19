from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import RouteQuery, question_router
from graph.chains.mode_router import route_with_mode_detection
from graph.consts import (
    GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH, 
    GENERATE_QUIZ, GENERATE_FLASHCARDS,
    MODE_QNA, MODE_QUIZ, MODE_FLASHCARD
)
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.nodes.quiz_node import generate_quiz
from graph.nodes.flashcard_node import generate_flashcards
from graph.state import GraphState

load_dotenv()


def route_by_mode_and_source(state: GraphState) -> str:
    """
    Route based on detected mode and data source
    """
    print("---ROUTE BY MODE AND SOURCE---")
    
    # Get user input (could be question or request)
    user_input = state["question"]
    
    # Detect mode, subject, and routing
    route_result = route_with_mode_detection(user_input)
    
    # Update state with detected information
    state["mode"] = route_result.mode
    state["subject"] = route_result.subject
    
    print(f"---DETECTED MODE: {route_result.mode}---")
    print(f"---DETECTED SUBJECT: {route_result.subject}---")
    print(f"---ROUTE TO: {route_result.datasource}---")
    
    # Route to data source first (always need to retrieve documents)
    if route_result.datasource == "websearch":
        return WEBSEARCH
    else:
        return RETRIEVE


def decide_generation_type(state: GraphState) -> str:
    """
    Decide what type of content to generate based on mode
    """
    print("---DECIDE GENERATION TYPE---")
    
    mode = state.get("mode", MODE_QNA)
    
    # Check if we have enough documents for quiz/flashcard generation
    documents = state.get("documents", [])
    if mode in [MODE_QUIZ, MODE_FLASHCARD] and len(documents) < 1:
        print("---INSUFFICIENT DOCUMENTS FOR QUIZ/FLASHCARD GENERATION, TRYING WEB SEARCH---")
        return WEBSEARCH
    
    if state.get("web_search", False):
        print("---DOCUMENTS NOT RELEVANT, INCLUDE WEB SEARCH---")
        return WEBSEARCH
    
    # Route based on mode
    if mode == MODE_QUIZ:
        print("---GENERATE QUIZ---")
        return GENERATE_QUIZ
    elif mode == MODE_FLASHCARD:
        print("---GENERATE FLASHCARDS---")
        return GENERATE_FLASHCARDS
    else:  # MODE_QNA or default
        print("---GENERATE ANSWER---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    """
    Grade generation for QNA mode only
    """
    print("---CHECK HALLUCINATIONS---")
    
    mode = state.get("mode", MODE_QNA)
    
    # Only apply grading for QNA mode
    if mode != MODE_QNA:
        print(f"---SKIPPING GRADING FOR {mode.upper()} MODE---")
        return "useful"
    
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    # Check hallucinations
    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"


# Create workflow
workflow = StateGraph(GraphState)

# Add all nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(GENERATE_QUIZ, generate_quiz)
workflow.add_node(GENERATE_FLASHCARDS, generate_flashcards)

# Set entry point with mode-based routing
workflow.set_conditional_entry_point(
    route_by_mode_and_source,
    {
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
    },
)

# From retrieve, always grade documents
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

# From grade_documents, decide what type of generation based on mode
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_generation_type,
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
        GENERATE_QUIZ: GENERATE_QUIZ,
        GENERATE_FLASHCARDS: GENERATE_FLASHCARDS,
    },
)

# Regular QNA generation flow with grading
workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": WEBSEARCH,
    },
)

# Quiz and flashcard generation go directly to END
workflow.add_edge(GENERATE_QUIZ, END)
workflow.add_edge(GENERATE_FLASHCARDS, END)

# Web search flows
workflow.add_conditional_edges(
    WEBSEARCH,
    decide_generation_type,
    {
        GENERATE: GENERATE,
        GENERATE_QUIZ: GENERATE_QUIZ,
        GENERATE_FLASHCARDS: GENERATE_FLASHCARDS,
    },
)

# Compile the graph
app = workflow.compile()