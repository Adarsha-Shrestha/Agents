import random
from typing import Dict, Any
from graph.state import GraphState


def generate_conversational_response(state: GraphState) -> Dict[str, Any]:
    """
    Generate simple responses for conversational queries
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with conversational response
    """
    question = state["question"].lower().strip()
    
    # Define response patterns
    greeting_responses = [
        "Hello! I'm here to help you with questions about DataMining, Networks, or general topics. What would you like to know?",
        "Hi there! I can help you find information from your study materials or search the web. What's your question?",
        "Hello! Ready to help with your DataMining and Network questions, or anything else you'd like to know.",
    ]
    
    how_are_you_responses = [
        "I'm doing well, thank you! I'm here and ready to help you with any questions about DataMining, Networks, or other topics.",
        "I'm great! How can I assist you today? I can help with DataMining, Network concepts, or search for other information.",
        "I'm doing fine, thanks for asking! What can I help you learn about today?",
    ]
    
    thanks_responses = [
        "You're welcome! Feel free to ask if you have any more questions about DataMining, Networks, or anything else.",
        "Happy to help! Let me know if you need assistance with anything else.",
        "Glad I could help! Ask me anything else you'd like to know.",
    ]
    
    general_responses = [
        "I'm here to help! Please ask me a specific question about DataMining, Networks, or any other topic you're curious about.",
        "Feel free to ask me questions about your study materials or anything else you'd like to know!",
        "I'm ready to assist you! What would you like to learn about today?",
    ]
    
    # Match patterns and generate responses
    if any(word in question for word in ["hello", "hi", "hey"]):
        response = random.choice(greeting_responses)
    elif any(phrase in question for phrase in ["how are you", "how do you do", "how's it going"]):
        response = random.choice(how_are_you_responses)
    elif any(word in question for word in ["thank", "thanks"]):
        response = random.choice(thanks_responses)
    else:
        response = random.choice(general_responses)
    
    return {
        "question": state["question"],
        "subject": state.get("subject"),
        "generation": response,
        "documents": [],
        "sources": [],
        "web_search": False,
        "loop_count": 0,
        "is_conversational": True
    }