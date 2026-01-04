SHARED_CSS = """
<style>
    /* 🎨 Custom Color Scheme */
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

    /* 🌌 Modern Dark Theme with Custom Colors */
    .stApp {
        background: linear-gradient(135deg, var(--bg-100) 0%, var(--bg-200) 50%, var(--primary-100) 100%) !important;
        color: var(--text-100);
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
        border-right: 1px solid var(--primary-200) !important;
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

    /* 🚀 Provider status */
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

    /* 🎨 Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-200) 0%, var(--primary-300) 50%, var(--accent-100) 100%) !important;
        color: var(--bg-100) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(172, 194, 239, 0.4) !important;
        background: linear-gradient(135deg, var(--primary-300) 0%, var(--accent-200) 50%, var(--primary-200) 100%) !important;
    }

    /* ⚡ Expander styling */
    .streamlit-expanderHeader {
        background: rgba(61, 90, 128, 0.3) !important;
        border: 1px solid var(--accent-100) !important;
        border-radius: 10px !important;
        color: var(--accent-200) !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background: rgba(31, 43, 62, 0.5) !important;
        border: 1px solid var(--bg-300) !important;
        border-radius: 0 0 10px 10px !important;
        color: var(--text-200) !important;
    }

    /* 📱 Chat message styling */
    .stChatMessage {
        background: rgba(31, 43, 62, 0.4) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border: 1px solid var(--bg-300) !important;
        overflow-x: auto !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ✨ Warning/Info/Success colors */
    .stAlert {
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    .stTextInput > div > div > input {
        background: rgba(31, 43, 62, 0.6) !important;
        border: 1px solid var(--bg-300) !important;
        border-radius: 12px !important;
        color: var(--text-100) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-200) !important;
        box-shadow: 0 0 0 2px rgba(206, 232, 255, 0.3) !important;
    }

    .stSpinner > div {
        border-color: var(--accent-200) transparent transparent transparent !important;
    }

    .stColumn {
        background: rgba(31, 43, 62, 0.3) !important;
        border: 1px solid var(--bg-300) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin: 0.5rem !important;
        backdrop-filter: blur(10px) !important;
    }

    .stBottom .st-emotion-cache-uomg8d {
        background: rgba(31, 43, 62, 0.95) !important;
        box-shadow:
          inset 30px 0 30px rgba(15, 28, 46, 0.3),
          inset -30px 0 30px rgba(15, 28, 46, 0.3);
        border-radius: 12px !important;
        width: 70% !important;
        min-width: 70% !important;
        margin: auto !important;
        bottom: 16px;
    }

    /* 📱 Responsive design */
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
"""


def apply_shared_styles():
    return SHARED_CSS
