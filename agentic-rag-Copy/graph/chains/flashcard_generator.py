from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Dict


class Flashcard(BaseModel):
    """Single flashcard with front and back"""
    front: str = Field(description="Question or prompt on the front of the card")
    back: str = Field(description="Answer or explanation on the back of the card")
    category: str = Field(description="Category or subtopic of this flashcard")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")
    tags: List[str] = Field(description="List of relevant tags for this flashcard")


class FlashcardSet(BaseModel):
    """Collection of flashcards"""
    flashcards: List[Flashcard] = Field(description="List of flashcards")
    topic: str = Field(description="Main topic of the flashcard set")
    total_cards: int = Field(description="Total number of flashcards generated")
    subject: str = Field(description="Academic subject area")


llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
structured_llm_flashcard = llm.with_structured_output(FlashcardSet)

flashcard_system_prompt = """You are an expert educational content creator specializing in generating effective flashcards for active recall and spaced repetition learning.

Your task is to create flashcards based on the provided academic documents. Follow these guidelines:

1. **Front of Card (Question/Prompt):**
   - Create clear, specific questions or prompts
   - Use different question types: definitions, explanations, examples, comparisons
   - Make questions concise but complete
   - Include key terms and concepts

2. **Back of Card (Answer):**
   - Provide comprehensive but concise answers
   - Include key details and context
   - Use clear, student-friendly language
   - Add examples or mnemonics when helpful

3. **Content Strategy:**
   - Cover the most important concepts from the material
   - Create cards for definitions, processes, relationships, and applications
   - Include both foundational and advanced concepts
   - Ensure cards test understanding, not just memorization

4. **Organization:**
   - Assign appropriate categories/subtopics
   - Add relevant tags for easy searching
   - Set appropriate difficulty levels
   - Ensure cards are atomic (one concept per card)

Generate {num_cards} flashcards that will help students master the provided content."""

flashcard_prompt = ChatPromptTemplate.from_messages([
    ("system", flashcard_system_prompt),
    ("human", """Topic: {topic}
Subject: {subject}

Documents:
{documents}

Number of flashcards to generate: {num_cards}

Please generate flashcards based on this content.""")
])

flashcard_generator: RunnableSequence = flashcard_prompt | structured_llm_flashcard


def generate_flashcards_from_documents(documents, topic="General", subject="General", num_cards=10):
    """
    Generate flashcards from documents
    
    Args:
        documents: List of document objects
        topic: Topic name for the flashcards
        subject: Subject area
        num_cards: Number of flashcards to generate
    
    Returns:
        FlashcardSet: Generated flashcard data
    """
    # Combine document content
    doc_content = "\n\n".join([doc.page_content for doc in documents])
    
    # Generate flashcards
    flashcard_result = flashcard_generator.invoke({
        "documents": doc_content,
        "topic": topic,
        "subject": subject,
        "num_cards": num_cards
    })
    
    return flashcard_result


# Utility functions for flashcard display and interaction
def display_flashcard(flashcard: Flashcard, show_answer=False):
    """Display a single flashcard"""
    print("=" * 50)
    print(f"📚 Category: {flashcard.category}")
    print(f"🎯 Difficulty: {flashcard.difficulty}")
    print(f"🏷️  Tags: {', '.join(flashcard.tags)}")
    print("-" * 50)
    print(f"❓ {flashcard.front}")
    
    if show_answer:
        print(f"\n💡 {flashcard.back}")
    print("=" * 50)


def flashcard_study_session(flashcards: List[Flashcard]):
    """Interactive flashcard study session"""
    print(f"🎓 Starting study session with {len(flashcards)} flashcards")
    print("Commands: 'show' to see answer, 'next' for next card, 'quit' to exit")
    
    for i, card in enumerate(flashcards, 1):
        print(f"\n📖 Card {i}/{len(flashcards)}")
        display_flashcard(card, show_answer=False)
        
        while True:
            command = input("\n> ").strip().lower()
            
            if command in ['show', 's']:
                print(f"\n💡 Answer: {card.back}")
                break
            elif command in ['next', 'n', '']:
                break
            elif command in ['quit', 'q']:
                print("👋 Study session ended!")
                return
            else:
                print("Commands: 'show', 'next', 'quit'")
    
    print("\n🎉 Study session completed! Great job!")