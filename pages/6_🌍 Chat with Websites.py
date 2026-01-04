import streamlit as st
import requests
import os
import sys
import re
import traceback

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="Chat with Website",
    page_icon="🔗",
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
        
        /* 💡 Website info styling */
        .website-info {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
            color: var(--text-200) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 🔗 URL item styling */
        .url-item {
            background: rgba(31, 43, 62, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            padding: 0.8rem !important;
            margin: 0.3rem 0 !important;
            color: var(--primary-300) !important;
            word-break: break-all !important;
        }
        
        /* 📋 Website details styling */
        .website-detail {
            background: rgba(31, 43, 62, 0.3) !important;
            border: 1px solid rgba(31, 43, 62, 0.4) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
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
            
        .st-emotion-cache-1w723zb {
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
    if "messages_web" not in st.session_state:
        st.session_state.messages_web = [
            {"role": "assistant", "content": "🔗 Hello! Add website URLs to analyze their content!"}
        ]
    
    if "current_provider_web" not in st.session_state:
        st.session_state.current_provider_web = None
    
    if "llm_instance_web" not in st.session_state:
        st.session_state.llm_instance_web = None
    
    if "last_error_web" not in st.session_state:
        st.session_state.last_error_web = None
    
    if "websites" not in st.session_state:
        st.session_state.websites = []
    
    if "website_contents" not in st.session_state:
        st.session_state.website_contents = {}

# ---------- HELPER FUNCTIONS ----------
def normalize_url(url):
    """Normalize URL"""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def fetch_website(url, max_chars=8000):
    """Fetch website content"""
    try:
        url = normalize_url(url)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Extract text from HTML
        html = response.text
        
        # Remove scripts and styles
        html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # Get text between tags
        text = re.sub(r'<[^>]+>', ' ', html)
        
        # Clean up
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Limit length
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # Get title
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1) if title_match else "No title"
        
        # Clean title
        title = title.replace('\n', ' ').strip()
        
        return {
            "success": True,
            "url": url,
            "title": title,
            "content": text,
            "length": len(text),
            "status_code": response.status_code
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout (15 seconds)", "url": url}
    except requests.exceptions.SSLError:
        return {"success": False, "error": "SSL Error", "url": url}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Failed", "url": url}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request Error: {str(e)[:100]}", "url": url}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)[:100]}", "url": url}

def build_prompt(query, website_results):
    """Build prompt with website content"""
    successful = [r for r in website_results if r.get("success", False)]
    
    if not successful:
        prompt = f"""The user asked: "{query}"

I tried to fetch websites but none were accessible.

Please provide a helpful response based on your general knowledge:"""
    else:
        context = "Based on these websites:\n\n"
        for i, website in enumerate(successful[:3], 1):  # Limit to 3 websites
            context += f"Website {i}: {website['title']}\n"
            context += f"URL: {website['url']}\n"
            context += f"Content preview: {website['content'][:600]}...\n\n"
        
        prompt = f"""The user asked: "{query}"

{context}

Please answer using information from the websites when possible.
If the answer isn't in the websites, use your general knowledge.
Mention which website(s) you're referencing.

Answer:"""
    
    return prompt

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
        
        elif "website" in error_lower or "url" in error_lower:
            st.markdown("""
            **Website Fetch Error Fix:**
            1. Check URL is correct
            2. Try with https:// prefix
            3. Website may block automated access
            4. Check internet connection
            
            **Test URLs:**
            • https://en.wikipedia.org
            • https://news.ycombinator.com
            • https://github.com
            """)
        
        elif "timeout" in error_lower:
            st.markdown("""
            **Timeout Fix:**
            1. Website may be slow or down
            2. Try different website
            3. Check your internet speed
            4. Website may block requests
            """)
        
        elif "connection" in error_lower or "network" in error_lower:
            st.markdown("""
            **Network Error Fix:**
            1. Check internet connection
            2. Try reloading page
            3. Check if website is down
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

# ---------- SIDEBAR CONFIGURATION ----------
def setup_sidebar():
    """Setup sidebar configuration"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0; margin-bottom: 0.5rem;">
            <h3 style="color: var(--accent-200); margin: 0; font-size: 1.6rem;">🌐 Website Chat</h3>
            <p style="color: var(--primary-300); font-size: 0.9rem; margin: 0.3rem 0 0 0;">Analyze Web Content</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear previous error
        if st.session_state.last_error_web:
            st.session_state.last_error_web = None
        
        # Import llm_providers
        try:
            from llm_providers import configure_llm_sidebar, get_llm_from_config
        except ImportError:
            st.error("llm_providers module not found")
            return None
        
        # Get LLM configuration
        try:
            config = configure_llm_sidebar(show_test_button=True)
            
            if config:
                current_provider = config.get("provider")
                api_key = config.get("api_key", "")
                
                # Check if provider changed
                if st.session_state.current_provider_web != current_provider:
                    st.session_state.current_provider_web = current_provider
                    if len(st.session_state.messages_web) > 1:
                        st.info(f"Provider changed to {current_provider}.")
                        st.session_state.messages_web = [
                            {"role": "assistant", "content": f"Switched to {current_provider}. Ready! 🔗"}
                        ]
                
                # Create LLM instance
                if api_key or current_provider == "Ollama (Local)":
                    with st.spinner(f"Configuring {current_provider}..."):
                        llm = get_llm_from_config(config)
                        
                        if llm:
                            st.session_state.llm_instance_web = llm
                            st.success(f"✅ {current_provider} configured")
                            
                            # Store provider info
                            st.session_state.current_provider_web = current_provider
                        else:
                            st.error(f"❌ Failed to initialize {current_provider}")
                            st.session_state.llm_instance_web = None
                
        except Exception as e:
            st.error(f"❌ Configuration error: {str(e)[:100]}")
            st.session_state.llm_instance_web = None
        
        st.markdown("---")
        
        # Website management
        st.markdown("### 🌐 Website URLs")
        
        # URL input
        new_url = st.text_input(
            "Enter Website URL",
            placeholder="https://example.com",
            help="Enter a valid website URL (include https://)",
            key="url_input"
        )
        
        # Quick URL buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🌐 Wikipedia", use_container_width=True, help="Add Wikipedia"):
                if "wikipedia.org" not in str(st.session_state.websites):
                    st.session_state.websites.append("https://en.wikipedia.org")
        with col2:
            if st.button("📰 Hacker News", use_container_width=True, help="Add Hacker News"):
                if "news.ycombinator.com" not in str(st.session_state.websites):
                    st.session_state.websites.append("https://news.ycombinator.com")
        with col3:
            if st.button("🐙 GitHub", use_container_width=True, help="Add GitHub"):
                if "github.com" not in str(st.session_state.websites):
                    st.session_state.websites.append("https://github.com")
        
        # Add URL button
        if st.button("➕ Add URL", use_container_width=True, type="primary"):
            if new_url and new_url.strip():
                url = normalize_url(new_url)
                if url not in st.session_state.websites:
                    st.session_state.websites.append(url)
                    st.success(f"✅ Added: {url[:50]}...")
                    st.rerun()
                else:
                    st.warning("URL already added")
        
        # Show websites
        if st.session_state.websites:
            st.markdown("**Added Websites:**")
            for url in st.session_state.websites[:5]:  # Show first 5
                st.markdown(f'''
                <div class="url-item">
                    🔗 {url}
                </div>
                ''', unsafe_allow_html=True)
            
            if len(st.session_state.websites) > 5:
                st.info(f"... and {len(st.session_state.websites) - 5} more")
        
        # Fetch button
        if st.session_state.websites:
            st.markdown("---")
            if st.button("🚀 Fetch Websites", use_container_width=True):
                with st.spinner("Fetching websites..."):
                    new_content = {}
                    for url in st.session_state.websites:
                        if url not in st.session_state.website_contents:
                            result = fetch_website(url)
                            new_content[url] = result
                        else:
                            new_content[url] = st.session_state.website_contents[url]
                    
                    st.session_state.website_contents = new_content
                    
                    successful = sum(1 for r in st.session_state.website_contents.values() if r.get("success", False))
                    total = len(st.session_state.websites)
                    
                    if successful > 0:
                        st.success(f"✅ Fetched {successful} of {total} websites")
                    else:
                        st.error("❌ Failed to fetch any websites")
                    st.rerun()
        
        # Troubleshooting expander
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **Website Issues:**
            
            1. **Website blocked** → Some sites block automated access
            2. **SSL errors** → Try different website
            3. **Slow loading** → Use popular websites
            4. **No content** → Website may use JavaScript
            
            **Quick Fixes:**
            - Wikipedia: Always works, great for testing
            - Hacker News: Simple text content
            - GitHub: Good for tech info
            - Use Groq for fastest analysis
            """)
        
        # Clear buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
                st.session_state.messages_web = [
                    {"role": "assistant", "content": "Chat cleared! Ready! 🔗"}
                ]
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear URLs", use_container_width=True, type="secondary"):
                st.session_state.websites = []
                st.session_state.website_contents = {}
                st.session_state.messages_web = [
                    {"role": "assistant", "content": "Websites cleared! Add new URLs to begin. 🌐"}
                ]
                st.rerun()
        
        return st.session_state.llm_instance_web

# ---------- MAIN APP ----------
def main():
    # Initialize session
    initialize_session()
    
    # Setup sidebar
    llm = setup_sidebar()
    
    # Header - MATCHING BASIC CHATBOT STYLE
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, var(--accent-200) 0%, var(--primary-300) 50%, var(--accent-100) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);">🌐 Chat with Websites</h1>
        <p style="color: var(--primary-300); font-size: 1.2rem; font-weight: 300;">Analyze and ask questions about website content</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current provider status
    current_provider = st.session_state.get("current_provider_web")
    if current_provider:
        if st.session_state.get("llm_instance_web"):
            pass
        else:
            st.markdown(f'<div class="provider-status provider-error">❌ {current_provider} Not Configured</div>', unsafe_allow_html=True)
    
    # Display website status
    if st.session_state.websites:
        successful = sum(1 for r in st.session_state.website_contents.values() if r.get("success", False))
        total = len(st.session_state.websites)
        
        if successful > 0:
            st.markdown(f'''
            <div class="website-info">
                <div style="color: var(--accent-200); font-size: 1.2rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 10px;">
                    🌐 Website Status
                </div>
                <div style="color: var(--text-200); line-height: 1.6;">
                    • URLs added: <strong style="color: var(--accent-200);">{total}</strong><br>
                    • Successfully fetched: <strong style="color: var(--accent-200);">{successful}</strong><br>
                    • Ask questions about the content
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("🌐 Websites added. Click 'Fetch Websites' in sidebar to load content.")
    else:
        st.info("🌐 Add website URLs in the sidebar to begin.")
    
    # Display last error if any
    if st.session_state.last_error_web:
        st.markdown(f'<div class="error-message">{st.session_state.last_error_web}</div>', unsafe_allow_html=True)
        display_error_help(st.session_state.last_error_web, current_provider)
    
    # Display chat messages
    for message in st.session_state.messages_web:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if llm and st.session_state.websites and st.session_state.website_contents:
        user_input = st.chat_input("Ask about the website content...", key="chat_input")
        
        if user_input:
            # Add user message
            st.session_state.messages_web.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Process and display AI response
            with st.chat_message("assistant"):
                with st.spinner("🔍 Analyzing website content..."):
                    try:
                        # Get website results
                        website_results = list(st.session_state.website_contents.values())
                        
                        # Build prompt
                        prompt = build_prompt(user_input, website_results)
                        
                        # Get response
                        from llm_providers import invoke_llm
                        response = invoke_llm(llm, prompt)
                        
                        # Display response
                        st.write(response)
                        
                        # Show website info
                        successful_sites = [r for r in website_results if r.get("success", False)]
                        if successful_sites and not (response.startswith("❌") or response.startswith("⚠️")):
                            with st.expander("📋 Website Details", expanded=False):
                                for site in successful_sites[:3]:
                                    st.markdown(f"""
                                    <div class="website-detail">
                                        <strong style="color: var(--accent-200);">{site['title']}</strong><br>
                                        <small style="color: var(--primary-300);">{site['url']}</small><br>
                                        <div style="color: var(--text-200); margin-top: 0.5rem;">
                                            📄 {site['length']} characters<br>
                                            ✅ Successfully loaded
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Add to chat history
                        st.session_state.messages_web.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)[:100]}"
                        st.error(error_msg)
                        st.session_state.last_error_web = error_msg
                        st.session_state.messages_web.append({"role": "assistant", "content": error_msg})
            
            # Rerun
            st.rerun()
    
    elif not llm:
        # Provider not configured - show help
        st.warning("Please configure an AI provider in the sidebar to start analyzing.")
        
        # Show provider options - UPDATED STYLING
        st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #00ff00; margin-bottom: 0.8rem;">⚡ Groq</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Fast web analysis</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Quick responses</li>
                    <li>30 free requests/minute</li>
                    <li>Great for multiple websites</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://console.groq.com/keys" target="_blank">🔑 Get Free Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #ffcc00; margin-bottom: 0.8rem;">🦙 Ollama</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Local analysis</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Privacy focused</li>
                    <li>No API limits</li>
                    <li>Process any content</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://ollama.ai" target="_blank">📥 Install Ollama</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: var(--accent-200); margin-bottom: 0.8rem;">🌐 Test Websites</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Always work:</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Wikipedia (en)</li>
                    <li>Hacker News</li>
                    <li>GitHub</li>
                    <li>Stack Overflow</li>
                </ul>
                <p style="margin-top: 1rem;">Click buttons in sidebar</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Example queries
        with st.expander("💡 Example Queries", expanded=True):
            st.markdown("""
            **With Wikipedia, you can ask:**
            
            • "What is artificial intelligence?"
            • "Tell me about the history of computers"
            • "What are the main programming languages?"
            • "Explain quantum computing"
            
            **With Hacker News:**
            • "What are the top stories about AI?"
            • "Latest tech news summary"
            • "Popular programming discussions"
            
            **With GitHub:**
            • "What are trending projects?"
            • "Explain repository structure"
            • "Popular open source licenses"
            """)
        
        # Installation instructions
        with st.expander("📦 Installation Help", expanded=False):
            st.markdown("""
            **Install required packages:**
            ```bash
            # For website fetching
            pip install requests
            
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
    
    elif not st.session_state.websites:
        st.info("🌐 Add website URLs in the sidebar to begin.")
    elif not st.session_state.website_contents:
        st.info("🌐 Click 'Fetch Websites' in sidebar to load content.")

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
        2. **Check internet connection**
        3. **Try Wikipedia** (always works)
        4. **Use Ollama** as fallback provider
        
        **Note:** Some websites block automated requests.
        Try these reliable sites:
        • https://en.wikipedia.org/wiki/Artificial_intelligence
        • https://news.ycombinator.com
        • https://github.com/topics
        """)