import streamlit as st
import sys
import os
from typing import Any, Dict
import traceback

# Ensure package path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_providers import configure_llm_sidebar, get_llm_from_config, invoke_llm
from pages_shared import llm_invoke, extract_text

st.set_page_config(
    page_title="ChatNet", 
    page_icon="🌐", 
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
        /* 🌌 Modern Dark Theme with Custom Colors */
        :root {
            --primary-100: #1F3A5F;
            --primary-200: #4d648d;
            --primary-300: #acc2ef;
            --accent-100: #3D5A80;
            --accent-200: #cee8ff;
            --text-100: #FFFFFF;
            --text-200: #e0e0e0;
            --bg-100: #0F1C2E;
            --bg-200: #1f2b3e;
            --bg-300: #374357;
        }


        /* 🌌 Modern Dark Theme with Gradient - EXACT SAME AS BASIC CHATBOT */
        .stApp {
            background: linear-gradient(135deg, var(--bg-100) 0%, var(--bg-200) 50%, var(--primary-100) 100%) !important;
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
            background: linear-gradient(180deg, var(--bg-200) 0%, var(--bg-100) 100%) !important;
            border-right: 1px solid var(--bg-300) !important;
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
        
        /* 💡 Info message styling - UPDATED COLORS */
        .info-message {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            color: var(--accent-200) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 🌐 Web search results - UPDATED COLORS */
        .search-result {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 15px !important;
            padding: 1.2rem !important;
            margin: 0.8rem 0 !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .search-title {
            color: var(--accent-200) !important;
            font-weight: bold !important;
            margin-bottom: 0.5rem !important;
            font-size: 1.1rem !important;
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
        
        /* 🔑 Tavily status */
        .tavily-status {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            color: var(--accent-200) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 🎨 Button styling - MATCHING BASIC CHATBOT */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-200) 0%, var(--primary-300) 50%, var(--accent-100) 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.8rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px var(--accent-100) !important;
        }
        
        /* ⚡ Expander styling */
        .streamlit-expanderHeader {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100)!important;
            border-radius: 10px !important;
            color: var(--accent-200) !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(31, 43, 62, 0.3) !important;
            border: 1px solid rgba(31, 43, 62, 0.4) !important;
            border-radius: 0 0 10px 10px !important;
            color: var(--text-200) !important;
        }
        
        /* 📱 Chat message styling */
        .stChatMessage {
            background: rgba(31, 43, 62, 0.3) !important;
            border-radius: 15px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border: 1px solid rgba(31, 43, 62, 0.4) !important;
            overflow-x: auto !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* ✨ Warning/Info/Success colors */
        .stAlert {
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input {
            background: rgba(31, 43, 62, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-200) !important;
            box-shadow: 0 0 0 2px rgba(125, 249, 255, 0.2) !important;
        }
        
        .stSpinner > div {
            border-color: var(--accent-200) transparent transparent transparent !important;
        }
        
        .stColumn {
            background: rgba(31, 43, 62, 0.3) !important;
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
            background: rgba(31, 43, 62, 0.95) !important;
            box-shadow:
              inset 30px 0 30px rgba(0, 0, 0, 0.12),
              inset -30px 0 30px rgba(0, 0, 0, 0.12);
            border-radius: 12px !important;
            width: 70% !important;
            min-width: 70% !important;
            margin: auto !important;
            bottom: 16px;
        }
        
        /* 📈 Source expander */
        .source-expander {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(31, 43, 62, 0.4) !important;
            border-radius: 10px !important;
            margin: 0.5rem 0 !important;
        }
        
        /* 🎯 Slider styling */
        .stSlider > div > div > div {
            background: rgba(125, 249, 255, 0.2) !important;
        }
        
        .stSlider > div > div > div > div {
            background: var(--accent-200) !important;
        }
            
            
        @media screen and (max-width: 360px),
               screen and (max-width: 767px),
               screen and (min-width: 768px) and (max-width: 991px) {
            
            div[data-testid="stChatMessageAvatarAssistant"] {
              display: none !important;
            }
            
            div[data-testid="stChatMessageContent"] {
              margin-left: 0 !important;
              padding-left: 0 !important;
            }
        }
            
        @media screen and (max-width: 767px) {
            .stBottom .st-emotion-cache-uomg8d {
                background: transparent !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                width: 100% !important;
                min-width: 100% !important;
                left: 0 !important;
                margin: 0 !important;
                bottom: 0 !important;
                padding: 0.5rem !important;
                transform: none !important;
            }
            .st-emotion-cache-6shykm {
                padding-bottom: 1.5rem !important;
            }
            .st-emotion-cache-1cei9z1 { 
                padding-top: 3rem !important;
            }
            
        }
        
        @media screen and (max-width: 360px) {
            .stBottom .st-emotion-cache-uomg8d {
                padding: 0.3rem !important;
                font-size: 0.9rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ---------- INITIALIZE SESSION STATE ----------
def initialize_session():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "🌐 Hello! I can search the web for current information. Ask me anything about recent events!"}
        ]
    
    if "current_provider" not in st.session_state:
        st.session_state.current_provider = None
    
    if "llm_instance" not in st.session_state:
        st.session_state.llm_instance = None
    
    if "last_error" not in st.session_state:
        st.session_state.last_error = None
    
    if "tavily_client" not in st.session_state:
        st.session_state.tavily_client = None

# ---------- SIDEBAR CONFIGURATION ----------
def setup_sidebar():
    """Setup sidebar configuration"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0; margin-bottom: 0.5rem;">
            <h3 style="color: var(--accent-200); margin: 0; font-size: 1.6rem;">🌐 Web Chat</h3>
            <p style="color: var(--primary-300); font-size: 0.9rem; margin: 0.3rem 0 0 0;">Internet-enabled AI</p>
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
                            {"role": "assistant", "content": f"Switched to {current_provider}. Ready to search the web! 🌐"}
                        ]
                
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
        
        # Web search configuration
        st.markdown("### 🌐 Web Search Settings")
        
        # Try to import Tavily
        try:
            from tavily import TavilyClient
            TAVILY_AVAILABLE = True
        except ImportError:
            TAVILY_AVAILABLE = False
            st.warning("Tavily not installed. Install: `pip install tavily-python`")
        
        # Tavily API key input
        if TAVILY_AVAILABLE:
            tavily_key = st.text_input(
                "Tavily API Key",
                type="password",
                placeholder="tvly-...",
                help="Get from https://tavily.com",
                key="tavily_api_key"
            )
            
            # Try to get from secrets
            if not tavily_key:
                tavily_key_from_secrets = st.secrets.get("TAVILY_API_KEY", "")
                if tavily_key_from_secrets:
                    tavily_key = tavily_key_from_secrets
            
            if tavily_key:
                try:
                    st.session_state.tavily_client = TavilyClient(api_key=tavily_key)
                    st.success("✅ Tavily connected")
                except Exception as e:
                    st.error(f"❌ Tavily error: {str(e)[:100]}")
            else:
                st.info("ℹ️ Add Tavily key for web search")
                st.markdown("[🔑 Get Tavily Key](https://tavily.com)")
        else:
            st.info("ℹ️ Web search requires Tavily package")
        
        # Search settings
        st.markdown("---")
        st.markdown("### 🔍 Search Options")
        
        search_depth = st.selectbox(
            "Search Depth",
            ["Basic (fast)", "Comprehensive (detailed)"],
            index=0,
            help="Basic for quick answers, Comprehensive for detailed research"
        )
        st.session_state.search_depth = search_depth
        
        max_results = st.slider(
            "Max Results",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="Number of web results to include"
        )
        st.session_state.max_results = max_results
        
        # Troubleshooting expander
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **Search Issues:**
            
            1. **No results found** → Try different keywords
            2. **Tavily API error** → Check API key is valid
            3. **Slow search** → Use Basic search depth
            4. **Package missing** → Install tavily-python
            
            **Quick Fixes:**
            - Get free Tavily key: https://tavily.com
            - Try Groq provider for fast responses
            - Check internet connection
            """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Chat cleared! Ready for web search! 🌐"}
            ]
            st.session_state.last_error = None
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
            elif "tavily" in error_lower.lower():
                st.markdown("[🔑 Get Tavily API Key](https://tavily.com)")
        
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

# ---------- INTERNET CHATBOT CLASS ----------
class InternetChatbot:
    def __init__(self):
        self.llm = st.session_state.get("llm_instance")
        self.provider = st.session_state.get("current_provider", "Unknown")
        self.tavily_client = st.session_state.get("tavily_client")
        
        if not self.llm:
            raise ValueError("LLM not configured. Please set up provider in sidebar.")
    
    def search_web(self, query: str):
        """Search the web using Tavily"""
        if not self.tavily_client:
            return None, "Web search not available. Please add Tavily API key in sidebar."
        
        try:
            # Determine search depth
            search_depth = st.session_state.get("search_depth", "Basic (fast)")
            depth = "basic" if "Basic" in search_depth else "advanced"
            
            max_results = st.session_state.get("max_results", 3)
            
            # Perform search
            response = self.tavily_client.search(
                query=query,
                search_depth=depth,
                max_results=max_results
            )
            
            if response and "results" in response:
                return response["results"], None
            else:
                return None, "No results found"
                
        except Exception as e:
            return None, f"Search error: {str(e)[:100]}"
    
    def build_prompt_with_context(self, query: str, search_results=None, search_error=None):
        """Build prompt with web search context"""
        if search_error:
            prompt = f"""The user asked: "{query}"

Note: Web search failed with error: {search_error}

Provide a helpful response based on your general knowledge:"""
        
        elif search_results:
            # Format search results
            context = ""
            for i, result in enumerate(search_results[:3], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content')
                url = result.get('url', '')
                
                context += f"\n\nResult {i}: {title}\n"
                if url:
                    context += f"URL: {url}\n"
                context += f"Content: {content[:500]}..."
            
            prompt = f"""The user asked: "{query}"

Based on the following web search results, provide a comprehensive answer. 
Cite sources when possible and mention if information is limited.

Search Results:
{context}

Please provide a well-structured answer:"""
        
        else:
            # No web search available
            prompt = f"""The user asked: "{query}"

Note: Web search is not available. Provide a helpful response based on your general knowledge.
If the question is about recent events, mention that you don't have current web access.

Response:"""
        
        return prompt
    
    def get_response(self, user_input: str) -> tuple:
        """Get response from LLM with web search"""
        if not self.llm:
            return "❌ LLM not configured. Please check sidebar settings.", None
        
        try:
            # Clear previous error
            st.session_state.last_error = None
            
            # Perform web search if Tavily is available
            search_results = None
            search_error = None
            
            if self.tavily_client:
                with st.spinner("🌐 Searching the web..."):
                    search_results, search_error = self.search_web(user_input)
            
            # Build prompt with context
            prompt = self.build_prompt_with_context(user_input, search_results, search_error)
            
            # Get response
            with st.spinner("🤔 Processing results..."):
                response = invoke_llm(self.llm, prompt)
            
            # Check if response is an error
            if response.startswith("❌") or response.startswith("⚠️"):
                st.session_state.last_error = response
                return response, search_results
            
            return response, search_results
            
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)[:150]}"
            st.session_state.last_error = error_msg
            return error_msg, None

# ---------- MAIN APP ----------
def main():
    # Initialize session
    initialize_session()
    
    # Setup sidebar
    llm = setup_sidebar()
    
    # Header - MATCHING BASIC CHATBOT STYLE
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, var(--accent-200) 0%, var(--primary-300) 50%, var(--accent-100) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);">🌐 Internet-Enabled Chatbot</h1>
        <p style="color: var(--primary-300); font-size: 1.2rem; font-weight: 300;">Accesses live web data for current information</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current provider status
    current_provider = st.session_state.get("current_provider")
    if current_provider:
        if st.session_state.get("llm_instance"):
            pass
        else:
            st.markdown(f'<div class="provider-status provider-error">❌ {current_provider} Not Configured</div>', unsafe_allow_html=True)
    
    # Web search status
    if st.session_state.get("tavily_client"):
        st.markdown('<div class="tavily-status">✅ Web search enabled</div>', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Web search disabled. Add Tavily API key in sidebar.")
    
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
        user_input = st.chat_input("Ask about current events, news, or recent information...", key="chat_input")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Get AI response with web search
            with st.chat_message("assistant"):
                try:
                    chatbot = InternetChatbot()
                    response, search_results = chatbot.get_response(user_input)
                    
                    # Display response
                    st.write(response)
                    
                    # Display search results if available
                    if search_results and not (response.startswith("❌") or response.startswith("⚠️")):
                        st.markdown("---")
                        st.markdown("#### 🔍 Web Sources")
                        for i, result in enumerate(search_results[:3], 1):
                            title = result.get('title', 'No title')
                            content = result.get('content', 'No content')[:200]
                            url = result.get('url', '')
                            
                            st.markdown(f"""
                            <div class="search-result">
                                <div class="search-title">Source {i}: {title}</div>
                                <div style="color: var(--text-200); margin-bottom: 0.5rem;">
                                    <strong>URL:</strong> <a href="{url}" target="_blank">{url}</a>
                                </div>
                                <div style="color: var(--primary-300);">
                                    <strong>Content:</strong> {content}...
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Add to history if not error
                    if not response.startswith("❌") and not response.startswith("⚠️"):
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
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
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #00ff00; margin-bottom: 0.8rem;">⚡ Groq</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Fastest for web search</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>30 free requests/minute</li>
                    <li>Quick processing</li>
                    <li>Great for live data</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://console.groq.com/keys" target="_blank">🔑 Get Free Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #ffcc00; margin-bottom: 0.8rem;">🦙 Ollama</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Local + Web</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Private browsing</li>
                    <li>Combine local & web</li>
                    <li>No API limits</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://ollama.ai" target="_blank">📥 Install Ollama</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: var(--accent-200); margin-bottom: 0.8rem;">🌐 Tavily</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Web search API</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Real-time web search</li>
                    <li>Reliable sources</li>
                    <li>Fast results</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://tavily.com" target="_blank">🔑 Get API Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Example questions
        with st.expander("🎯 Example Questions", expanded=True):
            st.markdown("""
            **With web search, I can answer:**
            
            • "What's the latest news about AI?"
            • "Current weather in New York?"
            • "Who won the recent football match?"
            • "Latest stock price of Tesla?"
            • "Recent space discoveries in 2024?"
            • "Best restaurants in Paris right now?"
            • "How to fix [current software issue]?"
            """)
        
        # Installation instructions
        with st.expander("📦 Installation Help", expanded=False):
            st.markdown("""
            **Install missing packages:**
            ```bash
            # For Tavily web search
            pip install tavily-python
            
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
        2. **Check API keys** are valid
        3. **Install missing packages**
        4. **Try without web search**
        """)