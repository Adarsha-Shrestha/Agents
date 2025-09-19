from typing import Any, Dict
from graph.chains.quiz_generator import generate_quiz_from_documents
from graph.state import GraphState


def generate_quiz(state: GraphState) -> Dict[str, Any]:
    """
    Generate quiz questions based on retrieved documents
    
    Args:
        state (GraphState): Current graph state
        
    Returns:
        Dict[str, Any]: Updated state with quiz data
    """
    print("---GENERATE QUIZ---")
    
    documents = state["documents"]
    subject = state.get("subject", "General")
    quiz_config = state.get("quiz_config", {})
    
    # Default quiz configuration
    num_questions = quiz_config.get("num_questions", 5)
    difficulty_mix = quiz_config.get("difficulty_mix", {"easy": 2, "medium": 2, "hard": 1})
    topic = state.get("question", f"{subject} Quiz")
    
    if not documents:
        print("---NO DOCUMENTS AVAILABLE FOR QUIZ GENERATION---")
        return {
            "quiz_data": [],
            "generation": "No documents available to generate quiz questions.",
            "question": state["question"],
            "subject": subject,
            "mode": state["mode"]
        }
    
    try:
        # Generate quiz questions
        quiz_result = generate_quiz_from_documents(
            documents=documents,
            topic=topic,
            num_questions=num_questions,
            difficulty_mix=difficulty_mix
        )
        
        print(f"---GENERATED {len(quiz_result.questions)} QUIZ QUESTIONS---")
        
        # Convert to serializable format
        quiz_data = []
        for q in quiz_result.questions:
            quiz_data.append({
                "question": q.question,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "difficulty": q.difficulty
            })
        
        # Generate summary message
        generation = f"Generated {len(quiz_data)} quiz questions on {topic}. " \
                    f"Difficulty distribution: {difficulty_mix}. Ready to start quiz!"
        
        return {
            "quiz_data": quiz_data,
            "generation": generation,
            "documents": documents,
            "question": state["question"],
            "subject": subject,
            "mode": state["mode"],
            "quiz_config": quiz_config
        }
        
    except Exception as e:
        print(f"---QUIZ GENERATION ERROR: {e}---")
        return {
            "quiz_data": [],
            "generation": f"Error generating quiz: {str(e)}",
            "question": state["question"],
            "subject": subject,
            "mode": state["mode"]
        }