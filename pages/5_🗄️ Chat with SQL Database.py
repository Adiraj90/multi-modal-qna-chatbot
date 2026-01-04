import streamlit as st
import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path
import traceback

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="ChatSQL",
    page_icon="🛢",
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
        
        /* 💡 Database info styling */
        .db-info {
            background: rgba(61, 90, 128, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
            color: var(--text-200) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 🛢 SQL code block styling */
        .sql-code {
            background: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid var(--accent-100) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            font-family: 'Courier New', monospace !important;
            white-space: pre-wrap !important;
            color: var(--accent-200) !important;
            overflow-x: auto !important;
        }
        
        /* 📊 Table styling */
        .dataframe {
            background: rgba(31, 43, 62, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
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
        
        /* 📋 Schema preview styling */
        .schema-preview {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(31, 43, 62, 0.4) !important;
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
    if "messages_sql" not in st.session_state:
        st.session_state.messages_sql = [
            {"role": "assistant", "content": "🗄️ Hello! I can help you query SQL databases using natural language!"}
        ]
    
    if "current_provider_sql" not in st.session_state:
        st.session_state.current_provider_sql = None
    
    if "llm_instance_sql" not in st.session_state:
        st.session_state.llm_instance_sql = None
    
    if "last_error_sql" not in st.session_state:
        st.session_state.last_error_sql = None
    
    if "database_path" not in st.session_state:
        st.session_state.database_path = None
    
    if "database_schema" not in st.session_state:
        st.session_state.database_schema = None

# ---------- HELPER FUNCTIONS ----------
def get_database_schema(db_path):
    """Get database schema"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]
        
        schema = {}
        for table in tables:
            # Get columns
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            
            schema[table] = [
                {"name": col[1], "type": col[2], "pk": col[5] == 1}
                for col in columns
            ]
        
        conn.close()
        return schema
    except Exception as e:
        return f"Error: {str(e)}"

def execute_sql_query(db_path, query):
    """Execute SQL query"""
    try:
        conn = sqlite3.connect(db_path)
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        return f"SQL error: {str(e)}"

def format_schema_for_prompt(schema):
    """Format schema for LLM prompt"""
    if isinstance(schema, str):
        return f"Schema error: {schema}"
    
    prompt = "Database Schema:\n\n"
    for table, columns in schema.items():
        prompt += f"Table '{table}':\n"
        for col in columns:
            pk = " (PRIMARY KEY)" if col["pk"] else ""
            prompt += f"  - {col['name']}: {col['type']}{pk}\n"
        prompt += "\n"
    
    return prompt

def generate_sql_from_natural_language(llm, schema_text, user_query):
    """Generate SQL from natural language"""
    from llm_providers import invoke_llm
    
    prompt = f"""Convert this natural language question to SQLite SQL.

{schema_text}

Rules:
1. Generate ONLY the SQL query, no explanations
2. Use SQLite syntax
3. Include LIMIT 10 if needed for large result sets
4. Use proper table joins when needed
5. Use correct column names from the schema

Question: {user_query}

SQL Query:"""
    
    response = invoke_llm(llm, prompt)
    
    # Clean SQL
    if "```sql" in response:
        response = response.split("```sql")[1].split("```")[0].strip()
    elif "```" in response:
        response = response.split("```")[1].split("```")[0].strip()
    
    # Ensure semicolon
    if not response.endswith(';'):
        response += ';'
    
    return response

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
        
        elif "sql" in error_lower or "database" in error_lower:
            st.markdown("""
            **SQL/Database Error Fix:**
            1. Check database file exists
            2. Verify database is not corrupted
            3. Check file permissions
            4. Try Chinook sample database
            """)
            
            if "chinook" in error_lower.lower():
                st.markdown("[📥 Download Chinook Database](https://github.com/lerocha/chinook-database)")
        
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
            <h3 style="color: var(--accent-200); margin: 0; font-size: 1.6rem;">🗄️ SQL Chat</h3>
            <p style="color: var(--primary-300); font-size: 0.9rem; margin: 0.3rem 0 0 0;">Query Databases with AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear previous error
        if st.session_state.last_error_sql:
            st.session_state.last_error_sql = None
        
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
                if st.session_state.current_provider_sql != current_provider:
                    st.session_state.current_provider_sql = current_provider
                    if len(st.session_state.messages_sql) > 1:
                        st.info(f"Provider changed to {current_provider}.")
                        st.session_state.messages_sql = [
                            {"role": "assistant", "content": f"Switched to {current_provider}. Ready! 🗄️"}
                        ]
                
                # Create LLM instance
                if api_key or current_provider == "Ollama (Local)":
                    with st.spinner(f"Configuring {current_provider}..."):
                        llm = get_llm_from_config(config)
                        
                        if llm:
                            st.session_state.llm_instance_sql = llm
                            st.success(f"✅ {current_provider} configured")
                            
                            # Store provider info
                            st.session_state.current_provider_sql = current_provider
                        else:
                            st.error(f"❌ Failed to initialize {current_provider}")
                            st.session_state.llm_instance_sql = None
                
        except Exception as e:
            st.error(f"❌ Configuration error: {str(e)[:100]}")
            st.session_state.llm_instance_sql = None
        
        st.markdown("---")
        
        # Database selection
        st.markdown("### 🗄️ Database Selection")
        
        db_option = st.radio(
            "Choose database:",
            ["Chinook Sample", "Custom SQLite"],
            index=0
        )
        
        if db_option == "Chinook Sample":
            # Check for Chinook
            chinook_path = Path(__file__).parent.parent / "assets" / "Chinook.db"
            
            if not chinook_path.exists():
                st.error("Chinook database not found")
                st.info("Download from: https://github.com/lerocha/chinook-database")
                st.markdown("[📥 Download Chinook](https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite)")
            else:
                st.session_state.database_path = str(chinook_path)
                st.success("✅ Using Chinook database")
                
                # Get schema
                with st.spinner("Loading schema..."):
                    schema = get_database_schema(str(chinook_path))
                    if isinstance(schema, dict):
                        st.session_state.database_schema = schema
                        st.info(f"✅ Found {len(schema)} tables")
                    else:
                        st.error(f"❌ {schema}")
        
        else:  # Custom database
            uploaded_file = st.file_uploader(
                "Upload SQLite Database",
                type=["db", "sqlite", "sqlite3"],
                help="Upload a SQLite database file"
            )
            
            if uploaded_file:
                # Save uploaded file
                temp_path = Path("temp_database.db")
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                st.session_state.database_path = str(temp_path)
                st.success("✅ Database uploaded")
                
                # Get schema
                with st.spinner("Loading schema..."):
                    schema = get_database_schema(str(temp_path))
                    if isinstance(schema, dict):
                        st.session_state.database_schema = schema
                        st.info(f"✅ Found {len(schema)} tables")
                    else:
                        st.error(f"❌ {schema}")
        
        # Show schema preview
        if st.session_state.database_schema and isinstance(st.session_state.database_schema, dict):
            st.markdown("---")
            st.markdown("### 📋 Database Schema")
            
            with st.expander("View Tables", expanded=False):
                tables = list(st.session_state.database_schema.keys())
                for table in tables[:10]:  # Show first 10 tables
                    cols = st.session_state.database_schema[table]
                    st.markdown(f"""
                    <div class="schema-preview">
                        <strong style="color: var(--accent-200);">{table}</strong><br>
                        <small style="color: var(--primary-300);">{len(cols)} columns</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Troubleshooting expander
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **SQL Issues:**
            
            1. **Database not found** → Check file path exists
            2. **SQL syntax errors** → AI may generate incorrect SQL
            3. **Slow queries** → Try Groq for faster responses
            4. **Connection issues** → Check database is not locked
            
            **Quick Fixes:**
            - Use Chinook sample database for testing
            - Ollama works best for local databases
            - Try different phrasing for questions
            """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.messages_sql = [
                {"role": "assistant", "content": "Chat cleared! Ready for SQL queries! 🗄️"}
            ]
            st.rerun()
        
        return st.session_state.llm_instance_sql

# ---------- MAIN APP ----------
def main():
    # Initialize session
    initialize_session()
    
    # Setup sidebar
    llm = setup_sidebar()
    
    # Header - MATCHING BASIC CHATBOT STYLE
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, var(--accent-200) 0%, var(--primary-300) 50%, var(--accent-100) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);">🗄️ Chat with SQL Databases</h1>
        <p style="color: var(--primary-300); font-size: 1.2rem; font-weight: 300;">Query databases using natural language</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display current provider status
    current_provider = st.session_state.get("current_provider_sql")
    if current_provider:
        if st.session_state.get("llm_instance_sql"):
            pass
        else:
            st.markdown(f'<div class="provider-status provider-error">❌ {current_provider} Not Configured</div>', unsafe_allow_html=True)
    
    # Display database status
    if st.session_state.database_path and st.session_state.database_schema:
        db_name = os.path.basename(st.session_state.database_path)
        table_count = len(st.session_state.database_schema)
        
        st.markdown(f'''
        <div class="db-info">
            <div style="color: var(--accent-200); font-size: 1.2rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 10px;">
                🗄️ Database Connected
            </div>
            <div style="color: var(--text-200); line-height: 1.6;">
                • Database: <strong style="color: var(--accent-200);">{db_name}</strong><br>
                • Tables: <strong style="color: var(--accent-200);">{table_count}</strong><br>
                • Ask questions in natural language
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Example queries for Chinook
        if "chinook" in db_name.lower():
            st.info("💡 **Try these example queries:**\n\n• Show all artists\n• List customers from Canada\n• Top 10 selling tracks\n• Artists with most albums")
    
    elif st.session_state.database_path:
        st.warning("⚠️ Database loaded but schema not extracted")
    else:
        st.info("🗄️ Select or upload a database in the sidebar to begin.")
    
    # Display last error if any
    if st.session_state.last_error_sql:
        st.markdown(f'<div class="error-message">{st.session_state.last_error_sql}</div>', unsafe_allow_html=True)
        display_error_help(st.session_state.last_error_sql, current_provider)
    
    # Display chat messages
    for message in st.session_state.messages_sql:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if llm and st.session_state.database_path and st.session_state.database_schema:
        user_input = st.chat_input("Ask a question about the database...", key="chat_input")
        
        if user_input:
            # Add user message
            st.session_state.messages_sql.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Process and display AI response
            with st.chat_message("assistant"):
                with st.spinner("🔍 Generating SQL query..."):
                    try:
                        # Generate SQL
                        schema_text = format_schema_for_prompt(st.session_state.database_schema)
                        sql = generate_sql_from_natural_language(llm, schema_text, user_input)
                        
                        # Execute SQL
                        results = execute_sql_query(st.session_state.database_path, sql)
                        
                        if isinstance(results, str):  # Error
                            response = f"❌ {results}"
                            st.error(response)
                        else:
                            # Display SQL
                            st.markdown("**Generated SQL:**")
                            st.markdown(f'<div class="sql-code">{sql}</div>', unsafe_allow_html=True)
                            
                            # Display results
                            if len(results) > 0:
                                st.markdown(f"**Results ({len(results)} rows):**")
                                st.dataframe(results, use_container_width=True, hide_index=True)
                                
                                # Generate explanation
                                from llm_providers import invoke_llm
                                explanation_prompt = f"""The user asked: "{user_input}"
The SQL query returned {len(results)} rows with columns: {', '.join(results.columns)}.

Provide a brief explanation of what these results show:"""
                                explanation = invoke_llm(llm, explanation_prompt)
                                
                                if not explanation.startswith("❌"):
                                    st.markdown("**Explanation:**")
                                    st.write(explanation)
                                    response = f"✅ Query executed successfully. Found {len(results)} rows.\n\n**Explanation:** {explanation}"
                                else:
                                    response = f"✅ Query executed successfully. Found {len(results)} rows."
                            else:
                                response = "✅ Query executed successfully. No results found."
                                st.info("No results found for the query.")
                        
                        # Add to chat history
                        st.session_state.messages_sql.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)[:100]}"
                        st.error(error_msg)
                        st.session_state.last_error_sql = error_msg
                        st.session_state.messages_sql.append({"role": "assistant", "content": error_msg})
            
            # Rerun
            st.rerun()
    
    elif not llm:
        # Provider not configured - show help
        st.warning("Please configure an AI provider in the sidebar to start querying.")
        
        # Show provider options - UPDATED STYLING
        st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #00ff00; margin-bottom: 0.8rem;">⚡ Groq</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Fast SQL generation</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Quick responses</li>
                    <li>30 free requests/minute</li>
                    <li>Accurate SQL generation</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://console.groq.com/keys" target="_blank">🔑 Get Free Key</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: #ffcc00; margin-bottom: 0.8rem;">🦙 Ollama</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Local SQL queries</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Query local databases</li>
                    <li>No API limits</li>
                    <li>Privacy guaranteed</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://ollama.ai" target="_blank">📥 Install Ollama</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(31, 43, 62, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem; height: 100%; backdrop-filter: blur(10px);">
                <h4 style="color: var(--accent-200); margin-bottom: 0.8rem;">🗄️ Chinook DB</h4>
                <p style="color: var(--text-200); margin-bottom: 1rem;"><strong>Sample database</strong></p>
                <ul style="color: var(--primary-300); padding-left: 1.2rem;">
                    <li>Music store database</li>
                    <li>Perfect for testing</li>
                    <li>11 tables, 15MB</li>
                </ul>
                <p style="margin-top: 1rem;"><a href="https://github.com/lerocha/chinook-database" target="_blank">📥 Download Database</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Example queries
        with st.expander("💡 Example Queries (Chinook DB)", expanded=True):
            st.markdown("""
            **With Chinook database, you can ask:**
            
            • "Show me all artists"
            • "List customers from Canada"
            • "What are the top 10 selling tracks?"
            • "Which artists have the most albums?"
            • "Show invoices from 2013"
            • "List all employees and their titles"
            • "What genres are available?"
            • "Show playlist names and track counts"
            """)
        
        # Installation instructions
        with st.expander("📦 Installation Help", expanded=False):
            st.markdown("""
            **Install required packages:**
            ```bash
            # For SQLite (included in Python)
            # No installation needed
            
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
    
    elif not st.session_state.database_path:
        st.info("🗄️ Select or upload a database in the sidebar to start querying.")

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
        2. **Download Chinook database** if missing
        3. **Try different provider**
        4. **Check database file** is valid SQLite
        
        **Still stuck?**
        - Verify SQLite file is not corrupted
        - Try different phrasing for queries
        - Use smaller databases first
        """)