from dotenv import load_dotenv
import random
from typing import Dict, Any

load_dotenv()

from graph.graph import app
from ingestion import AVAILABLE_SUBJECTS
from graph.consts import MODE_QNA, MODE_QUIZ, MODE_FLASHCARD


class StudySystem:
    """Enhanced study system with QNA, Quiz, and Flashcard features"""
    
    def __init__(self):
        self.current_quiz = None
        self.quiz_score = 0
        self.quiz_total = 0
        
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🎓 ADVANCED RAG STUDY SYSTEM 🎓")
        print("="*60)
        print(f"📚 Available subjects: {', '.join(AVAILABLE_SUBJECTS)}")
        print("\n🔧 Available modes:")
        print("1️⃣  Q&A Mode - Ask questions and get answers")
        print("2️⃣  Quiz Mode - Generate and take quizzes")
        print("3️⃣  Flashcard Mode - Create and study flashcards")
        print("4️⃣  Interactive Mode - Natural language input")
        print("5️⃣  Exit")
        print("="*60)
    
    def qna_mode(self):
        """Question and Answer mode"""
        print("\n📝 Q&A Mode - Ask questions about your subjects")
        print("Type 'back' to return to main menu")
        
        while True:
            question = input("\n❓ Your question: ").strip()
            if question.lower() == 'back':
                break
            if not question:
                continue
                
            subject = self.select_subject("Which subject is this question about?")
            if subject == 'back':
                continue
                
            try:
                response = app.invoke({
                    "question": question,
                    "subject": subject,
                    "mode": MODE_QNA
                })
                
                print(f"\n🤖 Answer: {response.get('generation', 'No answer generated')}")
                print(f"📚 Subject: {response.get('subject', 'Unknown')}")
                print(f"📄 Documents used: {len(response.get('documents', []))}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def quiz_mode(self):
        """Quiz generation and taking mode"""
        print("\n🧠 Quiz Mode - Test your knowledge")
        print("Commands: 'generate', 'take', 'back'")
        
        while True:
            command = input("\n🎯 Quiz command: ").strip().lower()
            
            if command == 'back':
                break
            elif command == 'generate':
                self.generate_quiz()
            elif command == 'take' and self.current_quiz:
                self.take_quiz()
            elif command == 'take' and not self.current_quiz:
                print("❌ No quiz available. Generate a quiz first.")
            else:
                print("Available commands: 'generate', 'take', 'back'")
    
    def generate_quiz(self):
        """Generate a new quiz"""
        print("\n📝 Generating Quiz...")
        
        subject = self.select_subject("Select subject for quiz:")
        if subject == 'back':
            return
            
        topic = input("📋 Enter topic/keywords (or press Enter for general): ").strip()
        if not topic:
            topic = f"{subject} concepts"
            
        try:
            num_questions = int(input("🔢 Number of questions (default 5): ") or "5")
        except ValueError:
            num_questions = 5
            
        try:
            response = app.invoke({
                "question": topic,
                "subject": subject,
                "mode": MODE_QUIZ,
                "quiz_config": {"num_questions": num_questions}
            })
            
            self.current_quiz = response.get('quiz_data', [])
            
            if self.current_quiz:
                print(f"\n✅ Generated {len(self.current_quiz)} questions on {topic}")
                print(f"📊 Subject: {subject}")
                print("Use 'take' command to start the quiz!")
            else:
                print("❌ Failed to generate quiz questions.")
                
        except Exception as e:
            print(f"❌ Error generating quiz: {e}")
    
    def take_quiz(self):
        """Take the generated quiz"""
        if not self.current_quiz:
            print("❌ No quiz available. Generate one first.")
            return
            
        print(f"\n🎯 Starting Quiz - {len(self.current_quiz)} Questions")
        print("="*50)
        
        self.quiz_score = 0
        self.quiz_total = len(self.current_quiz)
        
        for i, question_data in enumerate(self.current_quiz, 1):
            print(f"\n❓ Question {i}/{self.quiz_total}")
            print(f"🎚️  Difficulty: {question_data.get('difficulty', 'Unknown')}")
            print("-"*40)
            print(question_data['question'])
            print()
            
            # Display options
            for j, option in enumerate(question_data['options']):
                print(f"{chr(65+j)}. {option}")
            
            # Get user answer
            while True:
                answer = input("\n💭 Your answer (A/B/C/D): ").strip().upper()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print("Please enter A, B, C, or D")
            
            # Check answer
            correct_answer = question_data['correct_answer'].upper()
            if answer == correct_answer:
                print("✅ Correct!")
                self.quiz_score += 1
            else:
                print(f"❌ Wrong! Correct answer: {correct_answer}")
            
            print(f"💡 Explanation: {question_data.get('explanation', 'N/A')}")
            
            if i < self.quiz_total:
                input("\nPress Enter for next question...")
        
        # Show final results
        self.show_quiz_results()
    
    def show_quiz_results(self):
        """Display quiz results"""
        percentage = (self.quiz_score / self.quiz_total) * 100
        
        print("\n" + "="*50)
        print("🏆 QUIZ RESULTS 🏆")
        print("="*50)
        print(f"📊 Score: {self.quiz_score}/{self.quiz_total}")
        print(f"📈 Percentage: {percentage:.1f}%")
        
        if percentage >= 90:
            print("🌟 Excellent! Outstanding knowledge!")
        elif percentage >= 80:
            print("👍 Great job! Very good understanding!")
        elif percentage >= 70:
            print("👌 Good work! You're getting there!")
        elif percentage >= 60:
            print("📚 Not bad, but more study needed!")
        else:
            print("📖 Keep studying! You'll improve!")
        
        print("="*50)
    
    def flashcard_mode(self):
        """Flashcard generation and study mode"""
        print("\n🃏 Flashcard Mode - Create and study flashcards")
        print("Commands: 'generate', 'study', 'back'")
        
        current_flashcards = None
        
        while True:
            command = input("\n📚 Flashcard command: ").strip().lower()
            
            if command == 'back':
                break
            elif command == 'generate':
                current_flashcards = self.generate_flashcards()
            elif command == 'study' and current_flashcards:
                self.study_flashcards(current_flashcards)
            elif command == 'study' and not current_flashcards:
                print("❌ No flashcards available. Generate flashcards first.")
            else:
                print("Available commands: 'generate', 'study', 'back'")
    
    def generate_flashcards(self):
        """Generate new flashcards"""
        print("\n📝 Generating Flashcards...")
        
        subject = self.select_subject("Select subject for flashcards:")
        if subject == 'back':
            return None
            
        topic = input("📋 Enter topic/keywords (or press Enter for general): ").strip()
        if not topic:
            topic = f"{subject} concepts"
            
        try:
            num_cards = int(input("🔢 Number of flashcards (default 10): ") or "10")
        except ValueError:
            num_cards = 10
            
        try:
            response = app.invoke({
                "question": topic,
                "subject": subject,
                "mode": MODE_FLASHCARD,
                "flashcard_config": {"num_cards": num_cards}
            })
            
            flashcards = response.get('flashcard_data', [])
            
            if flashcards:
                print(f"\n✅ Generated {len(flashcards)} flashcards on {topic}")
                print(f"📊 Subject: {subject}")
                print("Use 'study' command to start studying!")
                return flashcards
            else:
                print("❌ Failed to generate flashcards.")
                return None
                
        except Exception as e:
            print(f"❌ Error generating flashcards: {e}")
            return None
    
    def study_flashcards(self, flashcards):
        """Study flashcard session"""
        print(f"\n🎓 Starting Flashcard Study Session")
        print(f"📚 {len(flashcards)} cards to study")
        print("Commands: 'show' (reveal answer), 'next' (next card), 'quit' (end session)")
        print("="*60)
        
        # Shuffle flashcards for better learning
        study_cards = flashcards.copy()
        random.shuffle(study_cards)
        
        for i, card in enumerate(study_cards, 1):
            print(f"\n📖 Card {i}/{len(study_cards)}")
            print(f"🏷️  Category: {card.get('category', 'General')}")
            print(f"🎯 Difficulty: {card.get('difficulty', 'Unknown')}")
            print(f"🏷️  Tags: {', '.join(card.get('tags', []))}")
            print("-"*50)
            print(f"❓ {card['front']}")
            
            answered = False
            while not answered:
                command = input("\n> ").strip().lower()
                
                if command in ['show', 's']:
                    print(f"\n💡 Answer: {card['back']}")
                    answered = True
                elif command in ['next', 'n', '']:
                    answered = True
                elif command in ['quit', 'q']:
                    print("👋 Study session ended!")
                    return
                else:
                    print("Commands: 'show', 'next', 'quit'")
        
        print("\n🎉 Study session completed! Great job studying!")
    
    def interactive_mode(self):
        """Natural language interactive mode"""
        print("\n🤖 Interactive Mode - Use natural language")
        print("Examples:")
        print("  - 'What is data mining?'")
        print("  - 'Create a quiz on network protocols'")
        print("  - 'Make flashcards for clustering algorithms'")
        print("Type 'back' to return to main menu")
        
        while True:
            user_input = input("\n💬 Say anything: ").strip()
            
            if user_input.lower() == 'back':
                break
            if not user_input:
                continue
            
            try:
                # Let the system automatically detect mode and subject
                response = app.invoke({"question": user_input})
                
                mode = response.get('mode', MODE_QNA)
                
                if mode == MODE_QNA:
                    print(f"\n🤖 Answer: {response.get('generation', 'No answer generated')}")
                    
                elif mode == MODE_QUIZ:
                    quiz_data = response.get('quiz_data', [])
                    if quiz_data:
                        print(f"\n✅ Generated {len(quiz_data)} quiz questions!")
                        take_quiz = input("🎯 Take the quiz now? (y/n): ").strip().lower()
                        if take_quiz in ['y', 'yes']:
                            self.current_quiz = quiz_data
                            self.take_quiz()
                    
                elif mode == MODE_FLASHCARD:
                    flashcard_data = response.get('flashcard_data', [])
                    if flashcard_data:
                        print(f"\n✅ Generated {len(flashcard_data)} flashcards!")
                        study_now = input("📚 Start study session now? (y/n): ").strip().lower()
                        if study_now in ['y', 'yes']:
                            self.study_flashcards(flashcard_data)
                
                print(f"\n📊 Mode: {mode.upper()}")
                print(f"📚 Subject: {response.get('subject', 'Auto-detected')}")
                print(f"📄 Documents used: {len(response.get('documents', []))}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def select_subject(self, prompt="Select subject:"):
        """Helper to select subject with validation"""
        print(f"\n{prompt}")
        for i, subject in enumerate(AVAILABLE_SUBJECTS, 1):
            print(f"{i}. {subject}")
        print("0. Auto-detect")
        print("b. Back")
        
        while True:
            choice = input("👉 Choose: ").strip().lower()
            
            if choice == 'b':
                return 'back'
            elif choice == '0':
                return None  # Auto-detect
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(AVAILABLE_SUBJECTS):
                        return AVAILABLE_SUBJECTS[idx]
                except ValueError:
                    pass
            
            print("Invalid choice. Please try again.")
    
    def run(self):
        """Main application loop"""
        print("🚀 Welcome to the Advanced RAG Study System!")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\n🎯 Select mode (1-5): ").strip()
                
                if choice == '1':
                    self.qna_mode()
                elif choice == '2':
                    self.quiz_mode()
                elif choice == '3':
                    self.flashcard_mode()
                elif choice == '4':
                    self.interactive_mode()
                elif choice == '5':
                    print("👋 Thank you for studying! Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-5.")
                    
            except KeyboardInterrupt:
                print("\n👋 Thank you for studying! Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    study_system = StudySystem()
    study_system.run()