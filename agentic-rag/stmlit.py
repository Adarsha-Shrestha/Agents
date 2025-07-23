import streamlit as st
import os
from dotenv import load_dotenv
import time
from typing import Dict, Any
import traceback

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Advanced RAG Chat",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .source-box {
        background-color: #808080;
        border-left: 4px solid #1f77b4;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .answer-box {
        background-color: #808080;
        border-left: 4px solid #28a745;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .step-indicator {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 8px;
        margin: 5px 0;
        border-radius: 3px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_app():
    """Initialize the RAG application"""
    try:    
        # Import and initialize the graph
        from graph.graph import app
        return app
    except Exception as e:
        st.error(f"Failed to initialize RAG system: {str(e)}")
        st.stop()

def format_documents(documents):
    """Format documents for display"""
    if not documents:
        return "No documents found"
    
    formatted_docs = []
    for i, doc in enumerate(documents, 1):
        content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
        # Truncate long content
        if len(content) > 300:
            content = content[:300] + "..."
        formatted_docs.append(f"**Source {i}:**\n{content}")
    
    return "\n\n".join(formatted_docs)

def process_query(app, query: str, progress_container):
    """Process the query and return results with progress updates"""
    try:
        progress_bar = progress_container.progress(0)
        status_text = progress_container.empty()
        
        # Custom callback to track progress
        class ProgressTracker:
            def __init__(self):
                self.steps = []
                self.current_step = 0
                self.total_steps = 5
            
            def update(self, step_name, progress_value):
                self.steps.append(step_name)
                self.current_step = progress_value
                progress_bar.progress(progress_value / self.total_steps)
                status_text.text(f"Step {progress_value}/{self.total_steps}: {step_name}")
        
        tracker = ProgressTracker()
        
        # Simulate progress updates (since we can't easily hook into the graph)
        tracker.update("Routing question...", 1)
        time.sleep(0.5)
        
        tracker.update("Retrieving documents...", 2)
        time.sleep(0.5)
        
        tracker.update("Grading document relevance...", 3)
        time.sleep(0.5)
        
        tracker.update("Generating answer...", 4)
        
        # Execute the graph
        result = app.invoke(input={"question": query})
        
        tracker.update("Complete!", 5)
        
        return result, tracker.steps
        
    except Exception as e:
        st.error(f"Error processing query: {str(e)}")
        return None, []

def main():
    # Header
    st.title("🦜 Advanced RAG Chat")
    st.markdown("Ask questions about AI agents, prompt engineering, and adversarial attacks!")
    
    # Initialize app
    if 'app' not in st.session_state:
        with st.spinner("Initializing RAG system..."):
            st.session_state.app = initialize_app()
    
    # Sidebar for settings and info
    with st.sidebar:
        st.header("Settings")
        
        # Model info
        st.subheader("Model Information")
        st.info("""
        **Knowledge Base:**
        - AI Agents
        - Prompt Engineering  
        - Adversarial Attacks on LLMs
        
        **Features:**
        - Document retrieval
        - Web search fallback
        - Hallucination detection
        - Self-correction
        """)
        
        # API Status
        st.subheader("API Status")
        openai_status = "✅ Connected" if os.getenv("OPENAI_API_KEY") else "❌ Not configured"
        tavily_status = "✅ Connected" if os.getenv("TAVILY_API_KEY") else "❌ Not configured"
        
        st.write(f"OpenAI: {openai_status}")
        st.write(f"Tavily: {tavily_status}")
        
        # Clear chat history
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Display answer
                st.markdown(f'<div class="answer-box">{message["content"]}</div>', unsafe_allow_html=True)
                
                # Display sources if available
                if "sources" in message:
                    with st.expander("📚 Sources", expanded=False):
                        st.markdown(f'<div class="source-box">{message["sources"]}</div>', unsafe_allow_html=True)
                
                # Display processing steps if available
                if "steps" in message:
                    with st.expander("🔄 Processing Steps", expanded=False):
                        for step in message["steps"]:
                            st.markdown(f'<div class="step-indicator">{step}</div>', unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about AI agents, prompt engineering, or adversarial attacks..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process the query
        with st.chat_message("assistant"):
            # Create containers for progress and response
            progress_container = st.empty()
            response_container = st.empty()
            
            # Process query
            result, steps = process_query(st.session_state.app, prompt, progress_container)
            
            # Clear progress
            progress_container.empty()
            
            if result:
                # Extract information from result
                answer = result.get("generation", "No answer generated")
                documents = result.get("documents", [])
                
                # Display answer
                response_container.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
                
                # Format sources
                sources_text = format_documents(documents)
                
                # Display sources
                with st.expander("📚 Sources", expanded=False):
                    st.markdown(f'<div class="source-box">{sources_text}</div>', unsafe_allow_html=True)
                
                # Display processing steps
                with st.expander("🔄 Processing Steps", expanded=False):
                    for step in steps:
                        st.markdown(f'<div class="step-indicator">{step}</div>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources_text,
                    "steps": steps
                })
            else:
                error_msg = "Sorry, I couldn't process your question. Please try again."
                response_container.markdown(f'<div class="error-box">{error_msg}</div>', unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

    # Example queries
    st.markdown("---")
    st.subheader("💡 Example Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What is agent memory?"):
            st.session_state.example_query = "What is agent memory?"
            st.rerun()
    
    with col2:
        if st.button("How does prompt engineering work?"):
            st.session_state.example_query = "How does prompt engineering work?"
            st.rerun()
    
    with col3:
        if st.button("What are adversarial attacks?"):
            st.session_state.example_query = "What are adversarial attacks on LLMs?"
            st.rerun()
    
    # Handle example queries
    if hasattr(st.session_state, 'example_query'):
        example_query = st.session_state.example_query
        delattr(st.session_state, 'example_query')
        
        # Add to chat and process
        st.session_state.messages.append({"role": "user", "content": example_query})
        st.rerun()

if __name__ == "__main__":
    main()