import streamlit as st

st.set_page_config(
    page_title="LangChain AI ChatHub",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ---------- Custom Styling ----------
st.markdown("""
    <style>
        /* 🌌 Modern Dark Theme with Gradient */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #FFFFFF;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* 🔷 Hide only the problematic elements, keep hamburger menu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Keep the main header visible */
        header {
            background: transparent !important;
            backdrop-filter: blur(20px) !important;
            border-bottom: none !important;
            height: 4rem !important;
        }
        
        html {
            scroll-behavior: smooth;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        .hero-section {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(25, 25, 112, 0.3), rgba(138, 43, 226, 0.3));
            border-radius: 30px;
            margin: 1rem auto;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            max-width: 1200px;
        }
        .st-emotion-cache-zy6yx3 {
            padding: 5rem 5rem 7rem !important;
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #7df9ff 0%, #9370db 50%, #00ffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .sub-title {
            font-size: 1.3rem;
            color: #b0b0ff;
            margin-bottom: 1.5rem;
            font-weight: 300;
            line-height: 1.5;
        }
        
        /* 🎨 Feature Cards - Enhanced with fixed sizing */
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 1.5rem;
            height: 240px; /* Fixed height */
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            margin-bottom: 1.5rem; /* Space between cards */
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(125, 249, 255, 0.5);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            z-index: 10; /* Ensure hovered card stays above others */
        }
        
        .feature-card h4 {
            color: #7df9ff;
            font-size: 1.3rem;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            gap: 10px;
            min-height: 3rem;
        }
        
        .feature-card p {
            color: #d0d0ff;
            line-height: 1.1;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            flex-grow: 1;
        }
        
        .api-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: auto; /* Push to bottom */
        }
        
        .api-tag {
            background: rgba(125, 249, 255, 0.15);
            color: #7df9ff;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            border: 1px solid rgba(125, 249, 255, 0.3);
        }
        
        /* 🔥 Quick Guide Cards - Horizontal Layout */
        .guide-card {
            background: linear-gradient(135deg, rgba(147, 112, 219, 0.15), rgba(0, 255, 255, 0.15));
            border: 1px solid rgba(147, 112, 219, 0.3);
            border-radius: 20px;
            padding: 1.5rem;
            height: 240px; /* Fixed height for all guide cards */
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .guide-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            border-color: rgba(125, 249, 255, 0.5);
        }
        
        .guide-step-number {
            font-size: 2rem;
            color: #7df9ff;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .guide-card h4 {
            color: #7df9ff;
            font-size: 1.2rem;
            margin-bottom: 0.8rem;
            min-height: 2.8rem;
        }
        
        .guide-card-content {
            color: #d0d0ff;
            font-size: 0.9rem;
            line-height: 1.4;
            flex-grow: 1;
        }
        
        /* 🏆 API Showcase - Consistent card sizing */
        .api-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .api-card:hover {
            transform: translateY(-5px);
            border-color: rgba(125, 249, 255, 0.5);
        }
        
        .api-icon {
            font-size: 2rem;
            margin-bottom: 0.8rem;
        }
        
        /* 📱 Responsive Design */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.2rem;
            }
            
            .hero-section {
                padding: 1.5rem 1rem;
            }
            
            .api-card {
                height: 180px;
                padding: 1.2rem;
            }
            
            .feature-card, .guide-card {
                height: auto;
                min-height: 200px;
            }
        }
        
        /* ✨ Section Headers */
        .section-header {
            text-align: center;
            margin: 2.5rem 0 1.5rem 0;
        }
        
        .section-header h2 {
            color: #7df9ff;
            font-size: 2rem;
            margin-bottom: 0.8rem;
        }
        
        .section-header p {
            color: #b0b0ff;
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* 📦 Grid container for feature cards */
        .features-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        @media (max-width: 992px) {
            .features-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .features-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
""", unsafe_allow_html=True)


# ---------- Hero Section ----------
st.markdown("""
<div class="hero-section">
    <h1 class="main-title">🤖 LangChain AI ChatHub</h1>
    <p class="sub-title">Unified Platform for Advanced AI Conversations • Multiple LLM Providers • Enterprise Ready</p>
</div>
""", unsafe_allow_html=True)

# ---------- API Showcase Section (3 columns with consistent sizing) ----------
st.markdown("""
<div class="section-header">
    <h2>🛠️ Powered by Leading AI Providers</h2>
    <p>Choose from multiple state-of-the-art LLM providers for optimal performance</p>
</div>
""", unsafe_allow_html=True)

# First Row: OpenAI, Gemini, Groq (3 equal columns)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="api-card">
        <div class="api-icon">🔷</div>
        <h4 style="color: #7df9ff; margin-bottom: 0.5rem; font-size: 1.2rem;">OpenAI</h4>
        <p style="color: #d0d0ff; font-size: 0.85rem; margin-bottom: 0.5rem;">GPT-4, GPT-3.5 Turbo</p>
        <div style="padding: 6px 14px; background: rgba(25, 25, 112, 0.3); border-radius: 20px;">
            <small style="color: #7df9ff; font-size: 0.8rem;">Premium API</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="api-card">
        <div class="api-icon">🌀</div>
        <h4 style="color: #4285f4; margin-bottom: 0.5rem; font-size: 1.2rem;">Google Gemini</h4>
        <p style="color: #d0d0ff; font-size: 0.85rem; margin-bottom: 0.5rem;">Gemini Pro & Flash</p>
        <div style="padding: 6px 14px; background: rgba(66, 133, 244, 0.1); border-radius: 20px;">
            <small style="color: #4285f4; font-size: 0.8rem;">Multimodal AI</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="api-card">
        <div class="api-icon">⚡</div>
        <h4 style="color: #00ff00; margin-bottom: 0.5rem; font-size: 1.2rem;">Groq</h4>
        <p style="color: #d0d0ff; font-size: 0.85rem; margin-bottom: 0.5rem;">Ultra-fast Inference</p>
        <div style="padding: 6px 14px; background: rgba(0, 255, 0, 0.1); border-radius: 20px;">
            <small style="color: #00ff00; font-size: 0.8rem;">High Speed</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Second Row: Anthropic and Ollama (centered, same size cards)
st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="api-card">
        <div class="api-icon">✨</div>
        <h4 style="color: #ff6b6b; margin-bottom: 0.5rem; font-size: 1.2rem;">Anthropic Claude</h4>
        <p style="color: #d0d0ff; font-size: 0.85rem; margin-bottom: 0.5rem;">Claude 3 Series</p>
        <div style="padding: 6px 14px; background: rgba(255, 107, 107, 0.1); border-radius: 20px;">
            <small style="color: #ff6b6b; font-size: 0.8rem;">Advanced Reasoning</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="api-card">
        <div class="api-icon">🦙</div>
        <h4 style="color: #ffcc00; margin-bottom: 0.5rem; font-size: 1.2rem;">Ollama Local</h4>
        <p style="color: #d0d0ff; font-size: 0.85rem; margin-bottom: 0.5rem;">TinyLlama, Llama 3</p>
        <div style="padding: 6px 14px; background: rgba(255, 204, 0, 0.1); border-radius: 20px;">
            <small style="color: #ffcc00; font-size: 0.8rem;">Private & Free</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- Quick Guide Section (HORIZONTAL CARDS) ----------
st.markdown("""
<div class="section-header">
    <h2>🚀 Quick Start Guide</h2>
    <p>Follow these simple steps to start using any chatbot</p>
</div>
""", unsafe_allow_html=True)

# Horizontal guide cards in a 5-column layout
guide_col1, guide_col2, guide_col3, guide_col4, guide_col5 = st.columns(5)

with guide_col1:
    st.markdown("""
    <div class="guide-card">
        <div class="guide-step-number">1️⃣</div>
        <h4>Choose a Chatbot Page</h4>
        <div class="guide-card-content">
            Select from 6 chatbot types in sidebar.
        </div>
    </div>
    """, unsafe_allow_html=True)

with guide_col2:
    st.markdown("""
    <div class="guide-card">
        <div class="guide-step-number">2️⃣</div>
        <h4>Select AI Provider</h4>
        <div class="guide-card-content">
            Choose from 5+ providers in sidebar dropdown.
        </div>
    </div>
    """, unsafe_allow_html=True)

with guide_col3:
    st.markdown("""
    <div class="guide-card">
        <div class="guide-step-number">3️⃣</div>
        <h4>Get Your API Key</h4>
        <div class="guide-card-content">
            Generate key from your chosen provider.
        </div>
    </div>
    """, unsafe_allow_html=True)

with guide_col4:
    st.markdown("""
    <div class="guide-card">
        <div class="guide-step-number">4️⃣</div>
        <h4>Test Connection</h4>
        <div class="guide-card-content">
            Enter API key & verify connection.
        </div>
    </div>
    """, unsafe_allow_html=True)

with guide_col5:
    st.markdown("""
    <div class="guide-card">
        <div class="guide-step-number">5️⃣</div>
        <h4>Start Chatting!</h4>
        <div class="guide-card-content">
            Begin using the chatbot immediately.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Link buttons below the guide cards
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #00ffff; text-decoration: none; margin: 0 1rem; font-size: 0.9rem;">🔑 OpenAI API Keys</a>
    <a href="https://console.groq.com" target="_blank" style="color: #00ffff; text-decoration: none; margin: 0 1rem; font-size: 0.9rem;">⚡ Groq Cloud</a>
    <a href="https://makersuite.google.com" target="_blank" style="color: #00ffff; text-decoration: none; margin: 0 1rem; font-size: 0.9rem;">🌀 Google AI Studio</a>
    <a href="https://console.anthropic.com" target="_blank" style="color: #00ffff; text-decoration: none; margin: 0 1rem; font-size: 0.9rem;">🤖 Anthropic Console</a>
</div>
""", unsafe_allow_html=True)

# ---------- Feature Cards (FIXED ALIGNMENT) ----------
st.markdown("""
<div class="section-header">
    <h2>✨ Advanced Features</h2>
    <p>Choose from 6 specialized chatbot implementations with multi-provider support</p>
</div>
""", unsafe_allow_html=True)

# Feature Cards in 3 columns with consistent sizing
feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🤖 Basic Chatbot</h4>
        <p>Engage in interactive conversations with any LLM provider.</p>
        <div class="api-tags">
            <span class="api-tag">OpenAI</span>
            <span class="api-tag">Groq</span>
            <span class="api-tag">Gemini</span>
            <span class="api-tag">Claude</span>
            <span class="api-tag">Ollama</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🌐 Internet-Enabled Chatbot</h4>
        <p>Access live web data with real-time search capabilities.</p>
        <div class="api-tags">
            <span class="api-tag">OpenAI</span>
            <span class="api-tag">Tavily API</span>
            <span class="api-tag">Real-time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📄 Document Intelligence</h4>
        <p>Chat with PDFs, Word docs, and text files using RAG.</p>
        <div class="api-tags">
            <span class="api-tag">All LLMs</span>
            <span class="api-tag">RAG</span>
            <span class="api-tag">Vector DB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🗄️ SQL Database Chat</h4>
        <p>Query databases using natural language with SQL generation.</p>
        <div class="api-tags">
            <span class="api-tag">OpenAI</span>
            <span class="api-tag">SQLAlchemy</span>
            <span class="api-tag">PostgreSQL</span>
            <span class="api-tag">MySQL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🧠 Context-Aware AI</h4>
        <p>Memory-enabled conversations with persistent context.</p>
        <div class="api-tags">
            <span class="api-tag">All LLMs</span>
            <span class="api-tag">Memory</span>
            <span class="api-tag">Conversation</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🌍 Website Analyzer</h4>
        <p>Extract and analyze content from any website.</p>
        <div class="api-tags">
            <span class="api-tag">OpenAI</span>
            <span class="api-tag">Web Scraping</span>
            <span class="api-tag">Summarization</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div style="text-align: center; margin: 3rem 0; padding: 1.5rem;">
    <p style="color: #b0b0ff; font-size: 0.95rem;">
        Powered by <b style="color: #7df9ff;">LangChain</b> and <b style="color: #ff6b6b;">Streamlit</b> | 
        Built with ❤️ by <b style="color: #ffcc00;">Aditya Raj</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="color: #7df9ff; font-size: 1.6rem;">🔮 AI ChatHub</h1>
        <p style="color: #b0b0ff; font-size: 0.85rem;">Multi-Provider AI Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Navigation")
    st.markdown("""
    **Select a chatbot to get started:**

    1. **🤖 Basic Chat** - Simple conversations  
    2. **🧠 Context-Aware** - Memory enabled  
    3. **🌐 Web Search** - Real-time info  
    4. **📄 Document Q&A** - PDF analysis  
    5. **🗄️ SQL Chat** - Database queries  
    6. **🌍 Website Chat** - Web content
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔗 Quick Links")
    st.markdown("""
    - [📖 Full Documentation](https://github.com/Adiraj90/multi-modal-qna-chatbot.git)
    - [🔑 OpenAI API Keys](https://platform.openai.com/api-keys)
    - [⚡ Groq Cloud](https://console.groq.com)
    - [🌀 Google AI Studio](https://makersuite.google.com)
    - [🤖 Anthropic Console](https://console.anthropic.com)
    - [🦙 Ollama Download](https://ollama.ai)
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 System Status")
    st.markdown("""
    **🟢 All Systems Operational**

    **Available Providers:**
    - OpenAI ✓
    - Groq ✓  
    - Gemini ✓
    - Claude ✓
    - Ollama ✓
    """)
    
    st.markdown("---")
    
    st.markdown("### ⭐ Support the Project")
    st.markdown("""
    If you find this project helpful, please consider giving it a star on GitHub!
    """)
    
    st.link_button(
        "⭐ Star on GitHub", 
        "https://github.com/Adiraj90/multi-modal-qna-chatbot.git",
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px;">
        <small style="color: #8888cc;">• Multi-LLM Support •</small>
        <br>
        <small style="color: #8888cc;">Built by Aditya Raj</small>
    </div>
    """, unsafe_allow_html=True)