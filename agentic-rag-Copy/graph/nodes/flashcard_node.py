from typing import Any, Dict
from graph.chains.flashcard_generator import generate_flashcards_from_documents
from graph.state import GraphState


def generate_flashcards(state: GraphState) -> Dict[str, Any]:
    """
    Generate flashcards based on retrieved documents
    
    Args:
        state (GraphState): Current graph state
        
    Returns:
        Dict[str, Any]: Updated state with flashcard data
    """
    print("---GENERATE FLASHCARDS---")
    
    documents = state["documents"]
    subject = state.get("subject", "General")
    flashcard_config = state.get("flashcard_config", {})
    
    # Default flashcard configuration
    num_cards = flashcard_config.get("num_cards", 10)
    topic = state.get("question", f"{subject} Study Cards")
    
    if not documents:
        print("---NO DOCUMENTS AVAILABLE FOR FLASHCARD GENERATION---")
        return {
            "flashcard_data": [],
            "generation": "No documents available to generate flashcards.",
            "question": state["question"],
            "subject": subject,
            "mode": state["mode"]
        }
    
    try:
        # Generate flashcards
        flashcard_result = generate_flashcards_from_documents(
            documents=documents,
            topic=topic,
            subject=subject,
            num_cards=num_cards
        )
        
        print(f"---GENERATED {len(flashcard_result.flashcards)} FLASHCARDS---")
        
        # Convert to serializable format
        flashcard_data = []
        for card in flashcard_result.flashcards:
            flashcard_data.append({
                "front": card.front,
                "back": card.back,
                "category": card.category,
                "difficulty": card.difficulty,
                "tags": card.tags
            })
        
        # Generate summary message
        generation = f"Generated {len(flashcard_data)} flashcards on {topic}. " \
                    f"Cards cover various difficulty levels and subtopics. Ready for study session!"
        
        return {
            "flashcard_data": flashcard_data,
            "generation": generation,
            "documents": documents,
            "question": state["question"],
            "subject": subject,
            "mode": state["mode"],
            "flashcard_config": flashcard_config
        }
        
    except Exception as e:
        print(f"---FLASHCARD GENERATION ERROR: {e}---")
        return {
            "flashcard_data": [],
            "generation": f"Error generating flashcards: {str(e)}",
            "question": state["question"],
            "subject": subject,
            "mode": state["mode"]
        }