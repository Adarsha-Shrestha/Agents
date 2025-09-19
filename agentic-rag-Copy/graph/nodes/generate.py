from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    subject = state.get("subject")
    sources = state.get("sources", [])

    generation = generation_chain.invoke({"context": documents, "question": question})
    
    return {
        "documents": documents, 
        "question": question, 
        "subject": subject,
        "generation": generation,
        "sources": sources
    }