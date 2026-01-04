import streamlit as st
import os
import tempfile
import sys
from pathlib import Path
from typing import List
import traceback

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="ChatPDF",
    page_icon="📄",
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
        
        /* 💡 Document info styling */
        .doc-info {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
            color: var(--text-200) !important;
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
        
        /* 📚 Document reference styling */
        .doc-reference {
            background: rgba(31, 43, 62, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
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
        
        .st-emotion-cache-1w723zb{
            padding-top: 2rem !important;
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
        
        /* 📄 File uploader styling */
        .uploadedFile {
            background: rgba(31, 43, 62, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            padding: 0.8rem !important;
            margin: 0.3rem 0 !important;
            color: var(--primary-300) !important;
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
    if "messages_doc" not in st.session_state:
        st.session_state.messages_doc = [
            {"role": "assistant", "content": "📄 Hello! Upload PDF documents to ask questions!"}
        ]
    
    if "current_provider_doc" not in st.session_state:
        st.session_state.current_provider_doc = None
    
    if "llm_instance_doc" not in st.session_state:
        st.session_state.llm_instance_doc = None
    
    if "last_error_doc" not in st.session_state:
        st.session_state.last_error_doc = None
    
    if "document_texts" not in st.session_state:
        st.session_state.document_texts = []
    
    if "processed_docs" not in st.session_state:
        st.session_state.processed_docs = False

# ---------- HELPER FUNCTIONS ----------
def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"Error reading text file: {str(e)}"

def process_documents(uploaded_files):
    """Process uploaded documents"""
    document_texts = []
    
    for uploaded_file in uploaded_files:
        temp_path = save_uploaded_file(uploaded_file)
        
        if uploaded_file.name.lower().endswith('.pdf'):
            text = extract_text_from_pdf(temp_path)
        elif uploaded_file.name.lower().endswith(('.txt', '.md')):
            text = extract_text_from_txt(temp_path)
        else:
            text = f"[Unsupported file type: {uploaded_file.name}]"
        
        if text and not text.startswith("Error reading"):
            document_texts.append({
                "name": uploaded_file.name,
                "text": text[:15000],  # Limit text length
                "size": len(text),
                "type": uploaded_file.type if hasattr(uploaded_file, 'type') else 'Unknown'
            })
        else:
            document_texts.append({
                "name": uploaded_file.name,
                "text": f"Could not extract text from {uploaded_file.name}",
                "size": 0,
                "type": "Error"
            })
        
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass
    
    return document_texts

def search_in_documents(query, document_texts, top_k=3):
    """Simple search in documents"""
    results = []
    query_lower = query.lower()
    
    for doc in document_texts:
        if doc["type"] == "Error":
            continue
            
        text_lower = doc["text"].lower()
        
        # Simple keyword matching
        if query_lower in text_lower:
            # Find context around match
            pos = text_lower.find(query_lower)
            start = max(0, pos - 200)
            end = min(len(doc["text"]), pos + 500)
            context = doc["text"][start:end]
            
            results.append({
                "name": doc["name"],
                "context": context,
                "relevance": 1.0
            })
        elif any(word in text_lower for word in query_lower.split()[:3]):
            # Partial match
            results.append({
                "name": doc["name"],
                "context": doc["text"][:500] + "...",
                "relevance": 0.5
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)
    return results[:top_k]

def build_prompt(query, search_results):
    """Build prompt with document context"""
    if not search_results:
        prompt = f"""The user asked: "{query}"

I have documents uploaded but couldn't find relevant information.

Please provide a helpful response based on your general knowledge:"""
    else:
        context = "Based on the following document excerpts:\n\n"
        for i, result in enumerate(search_results, 1):
            context += f"Document {i}: {result['name']}\n"
            context += f"Excerpt: {result['context'][:1000]}\n\n"
        
        prompt = f"""The user asked: "{query}"

{context}

Please answer the question using information from the documents when possible. 
If the answer isn't in the documents, use your general knowledge.

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
        
        elif "pdf" in error_lower or "pypdf" in error_lower:
            st.markdown("""
            **PDF Reading Error Fix:**
            1. Install PyPDF2 package
            2. Try a different PDF file
            3. Check if PDF is encrypted or corrupted
            4. Convert PDF to text file first
            """)
            
            st.code("pip install PyPDF2")
        
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

# ---------- SIDEBAR CONFIGURATION ----------
def setup_sidebar():
    """Setup sidebar configuration"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0; margin-bottom: 0.5rem;">
            <h3 style="color: var(--accent-200); margin: 0; font-size: 1.6rem;">📄 Document Chat</h3>
            <p style="color: var(--primary-300); font-size: 0.9rem; margin: 0.3rem 0 0 0;">Chat with PDF and Text Files</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear previous error
        if st.session_state.last_error_doc:
            st.session_state.last_error_doc = None
        
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
                if st.session_state.current_provider_doc != current_provider:
                    st.session_state.current_provider_doc = current_provider
                    # Clear messages on provider change
                    if len(st.session_state.messages_doc) > 1:
                        st.info(f"Provider changed to {current_provider}.")
                        st.session_state.messages_doc = [
                            {"role": "assistant", "content": f"Switched to {current_provider}. Ready! 😊"}
                        ]
                
                # Create LLM instance
                if api_key or current_provider == "Ollama (Local)":
                    with st.spinner(f"Configuring {current_provider}..."):
                        llm = get_llm_from_config(config)
                        
                        if llm:
                            st.session_state.llm_instance_doc = llm
                            st.success(f"✅ {current_provider} configured")
                            
                            # Store provider info
                            st.session_state.current_provider_doc = current_provider
                        else:
                            st.error(f"❌ Failed to initialize {current_provider}")
                            st.session_state.llm_instance_doc = None
                
        except Exception as e:
            st.error(f"❌ Configuration error: {str(e)[:100]}")
            st.session_state.llm_instance_doc = None
        
        st.markdown("---")
        
        # Document upload section
        st.markdown("### 📁 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            help="Upload PDF or text files (PDF, TXT, MD)",
            key="file_uploader_doc"
        )
        
        if uploaded_files:
            # Process if files changed
            current_names = [f.name for f in uploaded_files]
            previous_names = [f["name"] for f in st.session_state.document_texts] if st.session_state.document_texts else []
            
            if current_names != previous_names:
                with st.spinner("Processing documents..."):
                    document_texts = process_documents(uploaded_files)
                    st.session_state.document_texts = document_texts
                    st.session_state.processed_docs = True
                    
                    if document_texts:
                        st.success(f"✅ Processed {len(document_texts)} document(s)")
                    else:
                        st.error("❌ No documents could be processed")
        
        # Show uploaded files
        if st.session_state.document_texts:
            st.markdown("**Uploaded Files:**")
            for doc in st.session_state.document_texts:
                st.markdown(f"""
                <div class="uploadedFile">
                    📄 {doc['name']}<br>
                    <small style="color: var(--accent-200);">{doc['size']:,} characters</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Troubleshooting expander
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **Document Issues:**
            
            1. **PDF not readable** → Try different PDF or convert to text
            2. **File too large** → Split into smaller files
            3. **No text found** → Check if PDF has selectable text
            4. **PyPDF2 missing** → Install: `pip install PyPDF2`
            
            **Quick Fixes:**
            - Ollama: Best for local document processing
            - Use TXT files if PDF fails
            - Check file permissions
            """)
        
        # Clear buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
                st.session_state.messages_doc = [
                    {"role": "assistant", "content": "Chat cleared! Ready when you are! 😊"}
                ]
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Docs", use_container_width=True, type="secondary"):
                st.session_state.document_texts = []
                st.session_state.processed_docs = False
                st.session_state.messages_doc = [
                    {"role": "assistant", "content": "Documents cleared! Upload new files to begin. 📄"}
                ]
                st.rerun()
        
        return st.session_state.llm_instance_doc

# ---------- MAIN APP ----------
def main():
    # Initialize session
    initialize_session()
    
    # Setup sidebar
    llm = setup_sidebar()
    
    # Header - MATCHING BASIC CHATBOT STYLE
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, var(--accent-200) 0%, var(--primary-300) 50%, var(--accent-100) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);">📄 Chat with Documents</h1>
        <p style="color: var(--primary-300); font-size: 1.2rem; font-weight: 300;">Upload PDF/TXT files and ask questions about their content</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current provider status
    current_provider = st.session_state.get("current_provider_doc")
    if current_provider:
        if st.session_state.get("llm_instance_doc"):
            pass
        else:
            st.markdown(f'<div class="provider-status provider-error">❌ {current_provider} Not Configured</div>', unsafe_allow_html=True)
    
    # Display document status
    if st.session_state.processed_docs and st.session_state.document_texts:
        total_chars = sum(doc["size"] for doc in st.session_state.document_texts if doc["type"] != "Error")
        valid_docs = len([doc for doc in st.session_state.document_texts if doc["type"] != "Error"])
        
        st.markdown(f'''
        <div class="doc-info">
            <div style="color: var(--accent-200); font-size: 1.2rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 10px;">
                📄 Document Status
            </div>
            <div style="color: var(--text-200); line-height: 1.6;">
                • {valid_docs} document(s) ready<br>
                • {total_chars:,} total characters<br>
                • Ask questions about your documents
            </div>
        </div>
        ''', unsafe_allow_html=True)
    elif st.session_state.document_texts:
        st.info("📄 Documents uploaded but not processed.")
    else:
        st.info("📄 Upload documents in the sidebar to begin.")
    
    # Display last error if any
    if st.session_state.last_error_doc:
        st.markdown(f'<div class="error-message">{st.session_state.last_error_doc}</div>', unsafe_allow_html=True)
        display_error_help(st.session_state.last_error_doc, current_provider)
    
    # Display chat messages
    for message in st.session_state.messages_doc:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if llm and st.session_state.processed_docs and st.session_state.document_texts:
        user_input = st.chat_input("Ask a question about your documents...", key="chat_input")
        
        if user_input:
            # Add user message
            st.session_state.messages_doc.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Process and display AI response
            with st.chat_message("assistant"):
                with st.spinner("📖 Searching documents..."):
                    try:
                        # Search in documents
                        search_results = search_in_documents(user_input, st.session_state.document_texts)
                        
                        # Build prompt
                        prompt = build_prompt(user_input, search_results)
                        
                        # Get response from LLM
                        from llm_providers import invoke_llm
                        response = invoke_llm(llm, prompt)
                        
                        # Display response
                        st.write(response)
                        
                        # Show references if available
                        if search_results and not (response.startswith("❌") or response.startswith("⚠️")):
                            with st.expander("📚 Document References", expanded=False):
                                for i, result in enumerate(search_results, 1):
                                    st.markdown(f"""
                                    <div class="doc-reference">
                                        <strong style="color: var(--accent-200);">Document {i}: {result['name']}</strong><br>
                                        <div style="color: var(--primary-300); margin-top: 0.5rem;">
                                            {result['context'][:500]}...
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Add to chat history
                        st.session_state.messages_doc.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)[:100]}"
                        st.error(error_msg)
                        st.session_state.last_error_doc = error_msg
                        st.session_state.messages_doc.append({"role": "assistant", "content": error_msg})
            
            # Rerun to update display
            st.rerun()
    
    elif not llm:
        # Provider not configured - show help
        st.warning("Please configure an AI provider in the sidebar to start chatting.")
        
        # Show provider options - UPDATED STYLING
        st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #00ff00; margin-bottom: 0.8rem;">⚡ Groq</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Fast for large docs</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Quick processing</li>
                    <li>30 free requests/minute</li>
                    <li>Good for long documents</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://console.groq.com/keys" target="_blank">🔑 Get Free Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #ffcc00; margin-bottom: 0.8rem;">🦙 Ollama</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Best for documents</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Process files locally</li>
                    <li>No API limits</li>
                    <li>Privacy guaranteed</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://ollama.ai" target="_blank">📥 Install Ollama</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: var(--accent-200); margin-bottom: 0.8rem;">📄 PyPDF2</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Required for PDFs</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Extract PDF text</li>
                    <li>Essential for this app</li>
                    <li>Easy to install</li>
                </ul>
                <p style="margin-top: 1rem;">Install:</p>
                <code style="color: var(--accent-200);">pip install PyPDF2</code>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Supported file types
        with st.expander("📄 Supported File Types", expanded=True):
            st.markdown("""
            **PDF Files (.pdf):**
            • Research papers, reports, books
            • Must have selectable text (not scanned images)
            • Up to 50 pages recommended
            
            **Text Files (.txt, .md):**
            • Plain text documents
            • Markdown files
            • Code files
            • Maximum 50,000 characters
            
            **File Limits:**
            • Maximum 10 files per session
            • Maximum 5MB per file
            • Total size: 20MB limit
            """)
        
        # Installation instructions
        with st.expander("📦 Installation Help", expanded=False):
            st.markdown("""
            **Install required packages:**
            ```bash
            # For PDF processing
            pip install PyPDF2
            
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
    
    elif not st.session_state.processed_docs:
        st.info("📄 Upload and process documents in the sidebar to start asking questions.")

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
        2. **Install PyPDF2**: `pip install PyPDF2`
        3. **Try smaller files** or TXT files
        4. **Use Ollama** as fallback provider
        
        **Still stuck?**
        - Check if PDF has selectable text
        - Convert PDF to TXT using online tool
        - Try different browser
        """)