import streamlit as st
import sys
import os
from typing import Any, Dict
import traceback

# Ensure package path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streaming import StreamHandler
from llm_providers import configure_llm_sidebar, get_llm_from_config, invoke_llm
from pages_shared import llm_invoke, extract_text

st.set_page_config(
    page_title="Context Aware Chatbot", 
    page_icon="🧠", 
    layout="centered",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ---------- Custom Styling (EXACTLY MATCHING BASIC CHATBOT) ----------
st.markdown("""
    <style>
        /* 🌌 Modern Dark Theme with Gradient - EXACT SAME AS BASIC CHATBOT */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
            color: #FFFFFF;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            height: 100vh !important;
            overflow: hidden !important;
        }
            
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        header {
            background: transparent !important;
            backdrop-filter: blur(20px) !important;
            border-bottom: none !important;
            height: 4rem !important;
            display: none;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.1) !important;
        }
        
        .error-message {
            background: rgba(255, 107, 107, 0.15) !important;
            border: 1px solid rgba(255, 107, 107, 0.3) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            color: #ff6b6b !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 💡 Context info styling - UPDATED COLORS */
        .context-info {
            background: rgba(125, 249, 255, 0.15) !important;
            border: 1px solid rgba(125, 249, 255, 0.3) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
            color: #d0d0ff !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 🚀 Provider status - UPDATED COLORS */
        .provider-status {
            padding: 0.8rem 1.2rem !important;
            border-radius: 12px !important;
            margin: 1rem 0 !important;
            font-weight: bold !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .provider-success {
            background: rgba(0, 255, 0, 0.15) !important;
            border: 1px solid rgba(0, 255, 0, 0.3) !important;
            color: #00ff00 !important;
        }
        
        .provider-error {
            background: rgba(255, 107, 107, 0.15) !important;
            border: 1px solid rgba(255, 107, 107, 0.3) !important;
            color: #ff6b6b !important;
        }
        
        /* 🎨 Button styling - MATCHING BASIC CHATBOT */
        .stButton > button {
            background: linear-gradient(135deg, #7df9ff 0%, #9370db 50%, #00ffff 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.8rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(125, 249, 255, 0.3) !important;
        }
        
        /* ⚡ Expander styling */
        .streamlit-expanderHeader {
            background: rgba(125, 249, 255, 0.15) !important;
            border: 1px solid rgba(125, 249, 255, 0.3)!important;
            border-radius: 10px !important;
            color: #7df9ff !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 0 0 10px 10px !important;
            color: #d0d0ff !important;
        }
        
        /* 📱 Chat message styling */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 15px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        /* ✨ Warning/Info/Success colors */
        .stAlert {
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #7df9ff !important;
            box-shadow: 0 0 0 2px rgba(125, 249, 255, 0.2) !important;
        }
        
        .stSpinner > div {
            border-color: #7df9ff transparent transparent transparent !important;
        }
        
        .stColumn {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            padding: 1.5rem !important;
            margin: 0.5rem !important;
            backdrop-filter: blur(10px) !important;
        }  
        
        .st-emotion-cache-1cei9z1{
            padding-top: 2rem !important;
        }
        
        .stBottom .st-emotion-cache-uomg8d {
            background: rgba(40, 38, 70, 0.97) !important;
            box-shadow:
              inset 30px 0 30px rgba(0, 0, 0, 0.12),
              inset -30px 0 30px rgba(0, 0, 0, 0.12);
            border-radius: 12px !important;
            width: 70% !important;
            min-width: 70% !important;
            margin: auto !important;
            bottom: 16px;
        }
        
        /* 📋 Context preview styling */
        .context-preview {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
            padding: 0.8rem !important;
            margin: 0.3rem 0 !important;
            font-size: 0.9rem !important;
            color: #b0b0ff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- INITIALIZE SESSION STATE ----------
def initialize_session():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm a context-aware AI. I remember our conversation! 🤖✨"}
        ]
    
    if "context_history" not in st.session_state:
        st.session_state.context_history = []
    
    if "current_provider" not in st.session_state:
        st.session_state.current_provider = None
    
    if "llm_instance" not in st.session_state:
        st.session_state.llm_instance = None
    
    if "last_error" not in st.session_state:
        st.session_state.last_error = None

# ---------- SIDEBAR CONFIGURATION ----------
def setup_sidebar():
    """Setup sidebar configuration"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0; margin-bottom: 0.5rem;">
            <h3 style="color: #7df9ff; margin: 0; font-size: 1.6rem;">🧠 Context AI</h3>
            <p style="color: #b0b0ff; font-size: 0.9rem; margin: 0.3rem 0 0 0;">Basic Chatbot with Memory</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear previous error
        if st.session_state.get("last_error"):
            st.session_state.last_error = None
        
        # Get LLM configuration
        try:
            config = configure_llm_sidebar(show_test_button=True)
            
            if config:
                current_provider = config.get("provider")
                api_key = config.get("api_key", "")
                
                # Check if provider changed
                if st.session_state.get("current_provider") != current_provider:
                    st.session_state.current_provider = current_provider
                    # Clear messages on provider change
                    if st.session_state.messages and len(st.session_state.messages) > 1:
                        st.info(f"Provider changed to {current_provider}. Chat history cleared.")
                        st.session_state.messages = [
                            {"role": "assistant", "content": f"Switched to {current_provider}. I'll remember our conversation! 😊"}
                        ]
                        st.session_state.context_history = []
                
                # Create LLM instance
                if api_key or current_provider == "Ollama (Local)":
                    with st.spinner(f"Configuring {current_provider}..."):
                        llm = get_llm_from_config(config)
                        
                        if llm:
                            st.session_state.llm_instance = llm
                            st.success(f"✅ {current_provider} configured successfully")
                            
                            # Store provider info
                            st.session_state.current_provider = current_provider
                            st.session_state.llm_config = config
                        else:
                            st.error(f"❌ Failed to initialize {current_provider}")
                            st.session_state.llm_instance = None
                
        except Exception as e:
            st.error(f"❌ Configuration error: {str(e)[:100]}")
            st.session_state.llm_instance = None
        
        st.markdown("---")
        
        # Context settings
        st.markdown("### 🧠 Memory Settings")
        
        # Context length slider
        context_length = st.slider(
            "Conversation Memory",
            min_value=1,
            max_value=20,
            value=8,
            step=1,
            help="Number of previous messages to remember"
        )
        st.session_state.context_length = context_length
        
        # Show current context
        with st.expander("📋 Memory Preview", expanded=False):
            if st.session_state.context_history:
                for i, msg in enumerate(st.session_state.context_history[-5:], 1):
                    role = "You" if msg["role"] == "user" else "AI"
                    st.markdown(f"""
                    <div class="context-preview">
                        <strong>{i}. {role}:</strong> {msg['content'][:50]}...
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.text("No conversation memory yet")
        
        # Troubleshooting expander
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **Memory Issues:**
            
            1. **Forgetting context** → Increase memory slider
            2. **Slow responses** → Try different model/provider
            3. **Inconsistent replies** → Clear and restart conversation
            
            **Quick Fixes:**
            - Groq: Fastest for long conversations
            - Ollama: Best for unlimited memory
            - OpenAI: Most reliable for context
            """)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clear Memory", use_container_width=True, type="secondary"):
                st.session_state.context_history = []
                st.session_state.messages = [
                    {"role": "assistant", "content": "Memory cleared! Starting fresh. 😊"}
                ]
                st.success("Memory cleared!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
                st.session_state.messages = [
                    {"role": "assistant", "content": "Chat cleared! How can I help you? 😊"}
                ]
                st.rerun()
        
        return st.session_state.get("llm_instance")

# ---------- DISPLAY ERROR HELP ----------
def display_error_help(error_message: str, provider: str = None):
    """Display helpful error information"""
    if not error_message:
        return
    
    # Check for specific error types
    error_lower = error_message.lower()
    
    with st.expander("🛠️ Error Help", expanded=True):
        if "api key" in error_lower:
            st.markdown("""
            **Invalid API Key Fix:**
            1. Go to provider website to get key
            2. Copy key carefully (no spaces)
            3. Paste in sidebar
            4. Click outside the field to save
            """)
            
            if provider == "Groq":
                st.markdown("[🔑 Get Groq API Key](https://console.groq.com/keys)")
            elif provider == "OpenAI":
                st.markdown("[🔑 Get OpenAI API Key](https://platform.openai.com/api-keys)")
        
        elif "quota" in error_lower:
            st.markdown("""
            **Quota Exceeded Fix:**
            1. Check account billing/usage
            2. Wait for quota reset (usually monthly)
            3. Upgrade plan if needed
            4. Try different provider
            """)
            
            st.info("💡 Try Ollama (Local) - no API limits!")
        
        elif "connection" in error_lower or "network" in error_lower:
            st.markdown("""
            **Network Error Fix:**
            1. Check internet connection
            2. Try reloading page
            3. Check if provider is down
            4. Try different network
            """)
        
        elif "rate limit" in error_lower:
            st.markdown("""
            **Rate Limit Fix:**
            1. Wait 1 minute and try again
            2. Reduce request frequency
            3. Upgrade to higher tier
            4. Try different provider
            """)
        
        else:
            st.markdown("""
            **General Fix:**
            1. Check API key is valid
            2. Verify package is installed
            3. Restart the application
            4. Try different provider/model
            """)

# ---------- CONTEXT-AWARE CHATBOT CLASS ----------
class ContextChatbot:
    def __init__(self):
        self.llm = st.session_state.get("llm_instance")
        self.provider = st.session_state.get("current_provider", "Unknown")
        
        if not self.llm:
            raise ValueError("LLM not configured. Please set up provider in sidebar.")
    
    def build_prompt(self, user_input: str) -> str:
        """Build prompt with conversation history"""
        history = st.session_state.get("context_history", [])
        context_length = st.session_state.get("context_length", 8)
        
        # Keep context length exchanges
        context_exchanges = history[-context_length:] if len(history) > context_length else history
        
        # Build context string
        context_lines = []
        for exchange in context_exchanges:
            role = "Human" if exchange["role"] == "user" else "Assistant"
            context_lines.append(f"{role}: {exchange['content']}")
        
        context_str = "\n".join(context_lines) if context_lines else "No previous conversation."
        
        prompt = f"""You are a helpful AI assistant that remembers conversation history. 
Use the context below to provide relevant, consistent responses.

Previous conversation:
{context_str}

Human: {user_input}
Assistant: """
        
        return prompt
    
    def get_response(self, user_input: str) -> str:
        """Get response from LLM with comprehensive error handling"""
        if not self.llm:
            return "❌ LLM not configured. Please check sidebar settings."
        
        try:
            prompt = self.build_prompt(user_input)
            
            # Clear previous error
            st.session_state.last_error = None
            
            # Get response using invoke_llm from llm_providers
            response = invoke_llm(self.llm, prompt)
            
            # Check if response is an error
            if response.startswith("❌") or response.startswith("⚠️"):
                st.session_state.last_error = response
                return response
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)[:150]}"
            st.session_state.last_error = error_msg
            return error_msg

# ---------- MAIN APP ----------
def main():
    # Initialize session
    initialize_session()
    
    # Setup sidebar
    llm = setup_sidebar()
    
    # Header - MATCHING BASIC CHATBOT STYLE
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #7df9ff 0%, #9370db 50%, #00ffff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);">🧠 Context-Aware Chatbot</h1>
        <p style="color: #b0b0ff; font-size: 1.2rem; font-weight: 300;">Remembers conversation history for better responses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current provider status
    current_provider = st.session_state.get("current_provider")
    if current_provider:
        if st.session_state.get("llm_instance"):
            pass
        else:
            st.markdown(f'<div class="provider-status provider-error">❌ {current_provider} Not Configured</div>', unsafe_allow_html=True)
    
    # Context info
    context_length = st.session_state.get("context_length", 8)
    context_history_len = len(st.session_state.get("context_history", []))
    
    st.markdown(f'''
    <div class="context-info">
        <div style="color: #7df9ff; font-size: 1.2rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 10px;">
            🧠 Memory Status
        </div>
        <div style="color: #d0d0ff; line-height: 1.6;">
            • Remembering last <strong style="color: #7df9ff;">{context_length}</strong> messages<br>
            • Currently have <strong style="color: #7df9ff;">{context_history_len}</strong> messages in memory
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Display last error if any
    if st.session_state.get("last_error"):
        st.markdown(f'<div class="error-message">{st.session_state.last_error}</div>', unsafe_allow_html=True)
        display_error_help(st.session_state.last_error, current_provider)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if st.session_state.get("llm_instance"):
        user_input = st.chat_input("Type your message here...", key="chat_input")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.context_history.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking with context..."):
                    try:
                        chatbot = ContextChatbot()
                        response = chatbot.get_response(user_input)
                        
                        # Display response
                        st.write(response)
                        
                        # Add to history if not error
                        if not response.startswith("❌") and not response.startswith("⚠️"):
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            st.session_state.context_history.append({"role": "assistant", "content": response})
                        
                    except ValueError as e:
                        error_msg = str(e)
                        st.error(error_msg)
                        st.session_state.last_error = error_msg
                    except Exception as e:
                        error_msg = f"❌ Unexpected error: {str(e)[:100]}"
                        st.error(error_msg)
                        st.session_state.last_error = error_msg
            
            # Rerun to update display
            st.rerun()
    
    else:
        # Provider not configured - show help
        st.warning("Please configure an AI provider in the sidebar to start chatting.")
        
        # Show provider options - UPDATED STYLING
        st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #00ff00; margin-bottom: 0.8rem;">⚡ Groq</h4>
                <p style="color: #d0d0ff; margin-bottom: 1rem;"><strong>Best for conversations</strong></p>
                <ul style="color: #b0b0ff; padding-left: 1.2rem;">
                    <li>Fast context handling</li>
                    <li>30 requests/minute</li>
                    <li>Great memory retention</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://console.groq.com/keys" target="_blank">🔑 Get Free Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #ffcc00; margin-bottom: 0.8rem;">🦙 Ollama</h4>
                <p style="color: #d0d0ff; margin-bottom: 1rem;"><strong>Unlimited memory</strong></p>
                <ul style="color: #b0b0ff; padding-left: 1.2rem;">
                    <li>Run locally</li>
                    <li>No API limits</li>
                    <li>Long conversations</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://ollama.ai" target="_blank">📥 Install Ollama</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #7df9ff; margin-bottom: 0.8rem;">🔑 OpenAI</h4>
                <p style="color: #d0d0ff; margin-bottom: 1rem;"><strong>Reliable context</strong></p>
                <ul style="color: #b0b0ff; padding-left: 1.2rem;">
                    <li>Excellent memory</li>
                    <li>GPT-3.5/4 models</li>
                    <li>Consistent responses</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://platform.openai.com/api-keys" target="_blank">🔑 Get API Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Installation instructions
        with st.expander("📦 Installation Help", expanded=True):
            st.markdown("""
            **Install missing packages:**
            ```bash
            # For Groq
            pip install langchain-groq
            
            # For OpenAI  
            pip install langchain-openai
            
            # For Ollama
            pip install langchain-community ollama
            
            # For all providers
            pip install -r requirements.txt
            ```
            """)

# ---------- RUN APP ----------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"🚨 Application error: {str(e)[:200]}")
        
        # Show detailed error for debugging
        with st.expander("🔍 Debug Details", expanded=False):
            st.code(traceback.format_exc())
        
        st.info("""
        **Quick Recovery:**
        1. **Refresh the page** (F5 or Ctrl+R)
        2. **Clear memory** in sidebar
        3. **Try different provider**
        4. **Restart the app**
        """)