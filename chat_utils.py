import streamlit as st
from typing import Any, List, Dict
import logging

logger = logging.getLogger(__name__)

# ==================== CHAT MANAGEMENT ====================
def init_chat_session(page_name: str = "default"):
    """Initialize chat session for a specific page"""
    if f"messages_{page_name}" not in st.session_state:
        st.session_state[f"messages_{page_name}"] = [
            {"role": "assistant", "content": "Hello! How can I help you today? 😊"}
        ]
    
    if f"history_{page_name}" not in st.session_state:
        st.session_state[f"history_{page_name}"] = []

def display_chat_messages(page_name: str = "default"):
    """Display chat messages for current page"""
    messages_key = f"messages_{page_name}"
    
    if messages_key in st.session_state:
        for message in st.session_state[messages_key]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

def add_message(role: str, content: str, page_name: str = "default"):
    """Add message to chat history"""
    messages_key = f"messages_{page_name}"
    history_key = f"history_{page_name}"
    
    if messages_key not in st.session_state:
        st.session_state[messages_key] = []
    
    if history_key not in st.session_state:
        st.session_state[history_key] = []
    
    # Add to display messages
    st.session_state[messages_key].append({"role": role, "content": content})
    
    # Add to conversation history (for context)
    if role in ["user", "assistant"]:
        st.session_state[history_key].append({"role": role, "content": content})

def clear_chat_history(page_name: str = "default"):
    """Clear chat history for specific page"""
    messages_key = f"messages_{page_name}"
    history_key = f"history_{page_name}"
    
    if messages_key in st.session_state:
        st.session_state[messages_key] = [
            {"role": "assistant", "content": "Chat cleared! How can I help you? 😊"}
        ]
    
    if history_key in st.session_state:
        st.session_state[history_key] = []

# ==================== LLM UTILITIES ====================
def get_conversation_context(page_name: str = "default", max_turns: int = 6) -> str:
    """Get formatted conversation context"""
    history_key = f"history_{page_name}"
    
    if history_key not in st.session_state or not st.session_state[history_key]:
        return "No previous conversation."
    
    # Get recent history
    recent_history = st.session_state[history_key][-max_turns*2:]  # Each turn has user + assistant
    
    # Format history
    formatted = []
    for msg in recent_history:
        speaker = "Human" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{speaker}: {msg['content']}")
    
    return "\n".join(formatted)

def build_chat_prompt(user_input: str, system_prompt: str = None, page_name: str = "default") -> str:
    """Build prompt with system message and conversation history"""
    # System prompt
    if system_prompt is None:
        system_prompt = "You are a helpful AI assistant. Answer questions clearly and concisely."
    
    # Get conversation context
    context = get_conversation_context(page_name)
    
    # Build full prompt
    prompt = f"""{system_prompt}

Previous conversation:
{context}

Human: {user_input}
Assistant: """
    
    return prompt

# ==================== PROVIDER HELPERS ====================
def get_provider_status():
    """Check provider installation status"""
    import importlib.util
    
    providers = {
        "Groq": "langchain_groq",
        "OpenAI": "langchain_openai",
        "Google Gemini": "langchain_google_genai",
        "Anthropic Claude": "langchain_anthropic",
        "Ollama": "langchain_community"
    }
    
    status = {}
    for name, package in providers.items():
        try:
            spec = importlib.util.find_spec(package)
            status[name] = bool(spec)
        except:
            status[name] = False
    
    return status

def show_installation_guide():
    """Show installation guide for missing packages"""
    st.warning("Some packages are missing. Install with:")
    
    install_commands = {
        "Groq": "pip install langchain-groq",
        "OpenAI": "pip install langchain-openai",
        "Google Gemini": "pip install langchain-google-genai google-generativeai",
        "Anthropic Claude": "pip install langchain-anthropic anthropic",
        "Ollama": "pip install langchain-community ollama"
    }
    
    for provider, cmd in install_commands.items():
        st.code(cmd, language="bash")

# ==================== STREAMING SUPPORT ====================
class SimpleStreamHandler:
    """Simple streaming handler for LLM responses"""
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def on_llm_new_token(self, token: str, **kwargs):
        """Handle new token from streaming response"""
        self.text += token
        self.container.markdown(self.text + "▌")
    
    def on_llm_end(self, **kwargs):
        """Handle end of stream"""
        self.container.markdown(self.text)
