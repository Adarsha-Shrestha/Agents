# from dotenv import load_dotenv

# load_dotenv()

# from graph.graph import app
# from graph.utils.source_extractor import format_sources_for_display
# from graph.utils.conversational_detector import detect_conversational_query
# from graph.utils.conversational_responses import generate_conversational_response

# def main():
#     print("=== Advanced RAG with Subject Filtering ===")
#     print("Available subjects: DataMining, Network")
#     print("Leave subject empty for general search")
#     print("💡 Tip: Ask specific questions for better results!")
#     print("-" * 50)
    
#     while True:
#         question = input("\nEnter your question (or 'quit' to exit): ").strip()
        
#         if question.lower() == 'quit':
#             print("Goodbye! 👋")
#             break
            
#         if not question:
#             print("Please enter a valid question.")
#             continue
        
#         # Initialize input data with loop counter
#         input_data = {
#             "question": question,
#             "loop_count": 0,
#             "is_conversational": False
#         }
        
#         # Only ask for subject if the question seems to be informational
#         simple_greetings = ["hello", "hi", "hey", "thanks", "thank you", "how are you", "good morning", "good evening"]
#         is_likely_greeting = any(greeting in question.lower() for greeting in simple_greetings)
        
#         if not is_likely_greeting:
#             subject = input("Enter subject (DataMining/Network or press Enter for general): ").strip()
            
#             # Validate subject
#             valid_subjects = ["DataMining", "Network"]
#             if subject and subject not in valid_subjects:
#                 print(f"Warning: '{subject}' is not a recognized subject. Available: {valid_subjects}")
#                 subject = None
            
#             if subject:
#                 input_data["subject"] = subject
        
#         print(f"\nProcessing: '{question}'")
#         if input_data.get("subject"):
#             print(f"Subject filter: {input_data['subject']}")
        
#         try:
#             result = app.invoke(input=input_data)
            
#             # Check if it was a conversational response
#             if result.get("is_conversational", False):
#                 print("\n" + result.get("generation", "Hello! How can I help you?"))
#                 continue
            
#             print("\n" + "="*50)
#             print("ANSWER:")
#             print("="*50)
#             print(result.get("generation", "No answer generated"))
            
#             # Display sources only for informational queries
#             sources = result.get("sources", [])
#             if sources:
#                 print("\n" + "="*50)
#                 print("SOURCES:")
#                 print("="*50)
#                 formatted_sources = format_sources_for_display(sources)
#                 print(formatted_sources)
            
#             print("="*50)
            
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             print("💡 Try asking a more specific question about DataMining or Networks!")

# if __name__ == "__main__":
#     main()

# from dotenv import load_dotenv

# load_dotenv()

# from graph.graph import app
# from graph.utils.source_extractor import format_sources_for_display
# from graph.utils.conversational_detector import detect_conversational_query
# from graph.utils.conversational_responses import generate_conversational_response
# from graph.state import GraphState


# def main():
#     print("=== Advanced RAG with Subject Filtering ===")
#     print("Available subjects: DataMining, Network")
#     print("Leave subject empty for general search")
#     print("💡 Tip: Ask specific questions for better results!")
#     print("-" * 50)

#     valid_subjects = ["DataMining", "Network"]

#     while True:
#         question = input("\nEnter your question (or 'quit' to exit): ").strip()

#         if question.lower() == "quit":
#             print("Goodbye! 👋")
#             break

#         if not question:
#             print("Please enter a valid question.")
#             continue

#         # Use LLM-based conversational detector
#         detection = detect_conversational_query(question)

#         input_data = {
#             "question": question,
#             "loop_count": 0,
#             "is_conversational": detection["is_conversational"],
#         }

#         # If conversational → handle directly
#         if detection["is_conversational"]:
#             state = GraphState(question=question)
#             result = generate_conversational_response(state)
#             print("\n" + result["generation"])
#             continue

#         # Otherwise → ask for subject
#         subject = input("Enter subject (DataMining/Network or press Enter for general): ").strip()
#         if subject and subject not in valid_subjects:
#             print(f"⚠ '{subject}' is not a recognized subject. Available: {valid_subjects}")
#             subject = None

#         if subject:
#             input_data["subject"] = subject

#         print(f"\nProcessing: '{question}'")
#         if input_data.get("subject"):
#             print(f"Subject filter: {input_data['subject']}")

#         try:
#             result = app.invoke(input=input_data)

#             # Check again if graph flagged conversational
#             if result.get("is_conversational", False):
#                 print("\n" + result.get("generation", "Hello! How can I help you?"))
#                 continue

#             print("\n" + "=" * 50)
#             print("ANSWER:")
#             print("=" * 50)
#             print(result.get("generation", "No answer generated"))

#             sources = result.get("sources", [])
#             if sources:
#                 print("\n" + "=" * 50)
#                 print("SOURCES:")
#                 print("=" * 50)
#                 formatted_sources = format_sources_for_display(sources)
#                 print(formatted_sources)

#             print("=" * 50)

#         except Exception as e:
#             print(f"❌ Error: {e}")
#             print("💡 Try asking a more specific question about DataMining or Networks!")


# if __name__ == "__main__":
#     main()

# from dotenv import load_dotenv

# load_dotenv()

# from graph.graph import app
# from graph.utils.source_extractor import format_sources_for_display
# from graph.utils.conversational_detector import detect_conversational_query
# from graph.utils.conversational_responses import generate_conversational_response
# from graph.state import GraphState
# from app2 import QuizSystem  # Quiz Generation System
# from app3 import FlashcardSystem  # Flashcard Generation System



# def main():
#     print("=== Advanced RAG with Subject Filtering ===")
#     print("Available subjects: DataMining, Network")
#     print("Leave subject empty for general search")
#     print("💡 Tip: Ask specific questions for better results!")
#     print("-" * 50)

#     valid_subjects = ["DataMining", "Network"]
#     subject = None

#     # Let the user pick subject first
#     while True:
#         subject_choice = input("Select subject (DataMining/Network or press Enter for general): ").strip()
#         if not subject_choice:  # General mode
#             subject = None
#             print("Using general search (no subject filter).")
#             break
#         elif subject_choice in valid_subjects:
#             subject = subject_choice
#             print(f"Subject filter set to: {subject}")
#             break
#         else:
#             print(f"⚠ '{subject_choice}' is not a recognized subject. Available: {valid_subjects}")

#     # Main Q&A loop
#     while True:
#         question = input("\nEnter your question (or 'quit' to exit): ").strip()

#         if question.lower() == 'quit':
#             print("Goodbye! 👋")
#             break
          
#         if not question:
#             print("Please enter a valid question.")
#             continue
        
#         detection = detect_conversational_query(question)

#         input_data = {
#             "question": question,
#             "loop_count": 0,
#             "is_conversational": detection["is_conversational"],
#         }

#         # If conversational → handle directly
#         if detection["is_conversational"]:
#             state = GraphState(question=question)
#             result = generate_conversational_response(state)
#             print("\n" + result["generation"])
#             continue

#         if subject:
#             input_data["subject"] = subject

#         print(f"\nProcessing: '{question}'")
#         if input_data.get("subject"):
#             print(f"Subject filter: {input_data['subject']}")

#         try:
#             result = app.invoke(input=input_data)

#             # Check again if graph flagged conversational
#             if result.get("is_conversational", False):
#                 print("\n" + result.get("generation", "Hello! How can I help you?"))
#                 continue

#             print("\n" + "="*50)
#             print("ANSWER:")
#             print("="*50)
#             print(result.get("generation", "No answer generated"))

#             sources = result.get("sources", [])
#             if sources:
#                 print("\n" + "="*50)
#                 print("SOURCES:")
#                 print("="*50)
#                 formatted_sources = format_sources_for_display(sources)
#                 print(formatted_sources)

#             print("="*50)

#         except Exception as e:
#             print(f"❌ Error: {e}")
#             print("💡 Try asking a more specific question!")


# if __name__ == "__main__":
#     main()

from dotenv import load_dotenv

load_dotenv()

from graph.graph import app
from graph.utils.source_extractor import format_sources_for_display
from graph.utils.conversational_detector import detect_conversational_query
from graph.utils.conversational_responses import generate_conversational_response
from graph.state import GraphState
from app2 import QuizSystem  # Quiz Generation System
from app3 import FlashcardSystem  # Flashcard Generation System


def rag_system():
    print("=== Advanced RAG with Subject Filtering ===")
    print("Available subjects: DataMining, Network")
    print("Leave subject empty for general search")
    print("💡 Tip: Ask specific questions for better results!")
    print("-" * 50)

    valid_subjects = ["DataMining", "Network"]
    subject = None

    # Let the user pick subject first
    while True:
        subject_choice = input("Select subject (DataMining/Network or press Enter for general): ").strip()
        if not subject_choice:  # General mode
            subject = None
            print("Using general search (no subject filter).")
            break
        elif subject_choice in valid_subjects:
            subject = subject_choice
            print(f"Subject filter set to: {subject}")
            break
        else:
            print(f"⚠ '{subject_choice}' is not a recognized subject. Available: {valid_subjects}")

    # Main Q&A loop
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ").strip()

        if question.lower() == 'quit':
            print("Exiting RAG System 👋")
            break
          
        if not question:
            print("Please enter a valid question.")
            continue
        
        detection = detect_conversational_query(question)

        input_data = {
            "question": question,
            "loop_count": 0,
            "is_conversational": detection["is_conversational"],
        }

        # If conversational → handle directly
        if detection["is_conversational"]:
            state = GraphState(question=question)
            result = generate_conversational_response(state)
            print("\n" + result["generation"])
            continue

        if subject:
            input_data["subject"] = subject

        print(f"\nProcessing: '{question}'")
        if input_data.get("subject"):
            print(f"Subject filter: {input_data['subject']}")

        try:
            result = app.invoke(input=input_data)

            # Check again if graph flagged conversational
            if result.get("is_conversational", False):
                print("\n" + result.get("generation", "Hello! How can I help you?"))
                continue

            print("\n" + "="*50)
            print("ANSWER:")
            print("="*50)
            print(result.get("generation", "No answer generated"))

            sources = result.get("sources", [])
            if sources:
                print("\n" + "="*50)
                print("SOURCES:")
                print("="*50)
                formatted_sources = format_sources_for_display(sources)
                print(formatted_sources)

            print("="*50)

        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try asking a more specific question!")


def main():
    quiz_system = QuizSystem()
    flashcard_system = FlashcardSystem()

    while True:
        print("\n📚 Educational Systems Controller")
        print("1️⃣  Q&A (RAG System)")
        print("2️⃣  Quiz System")
        print("3️⃣  Flashcard System")
        print("4️⃣  Quit")
        
        choice = input("\nSelect system (1-4): ").strip()

        if choice == '1':
            print("\nLaunching Q&A RAG System...")
            rag_system()
        elif choice == '2':
            print("\nLaunching Quiz System...")
            quiz_system.interactive_mode()
        elif choice == '3':
            print("\nLaunching Flashcard System...")
            flashcard_system.interactive_mode()
        elif choice == '4':
            print("Thank you for using the Educational Systems! 👋")
            break
        else:
            print("⚠ Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
