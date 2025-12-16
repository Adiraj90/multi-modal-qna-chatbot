import os
import sys
import logging
import traceback
from typing import Dict, Any, List, Optional, Union
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== PROVIDER CONFIGURATION ====================
class ProviderConfig:
    PROVIDERS = {
        "Groq": {
            "package": "langchain_groq",
            "models": ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "meta-llama/llama-4-maverick-17b-128e-instruct", "mixtral-8x7b-32768", "gemma2-9b-it"],
            "requires_api_key": True,
            "help_text": "⚡ Ultra-fast inference (Recommended & Default)",
            "icon": "⚡",
            "secret_key": "GROQ_API_KEY",
            "api_website": "https://console.groq.com/keys",
            "default_model": "llama3-8b-8192",
            "class_name": "ChatGroq",
            "env_var": "GROQ_API_KEY"
        },
        "OpenAI": {
            "package": "langchain_openai",
            "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini"],
            "requires_api_key": True,
            "help_text": "Most popular AI models",
            "icon": "🔑",
            "secret_key": "OPENAI_API_KEY",
            "api_website": "https://platform.openai.com/api-keys",
            "default_model": "gpt-3.5-turbo",
            "class_name": "ChatOpenAI",
            "env_var": "OPENAI_API_KEY"
        },
        "Google Gemini": {
            "package": "langchain_google_genai",
            "models": ["gemini-pro", "gemini-1.5-pro"],
            "requires_api_key": True,
            "help_text": "Google's AI (Gemini)",
            "icon": "🌐",
            "secret_key": "GOOGLE_API_KEY",
            "api_website": "https://makersuite.google.com/app/apikey",
            "default_model": "gemini-pro",
            "class_name": "ChatGoogleGenerativeAI",
            "env_var": "GOOGLE_API_KEY"
        },
        "Anthropic Claude": {
            "package": "langchain_anthropic",
            "models": ["claude-3-haiku", "claude-3-opus", "claude-3-sonnet"],
            "requires_api_key": True,
            "help_text": "Anthropic models",
            "icon": "🧠",
            "secret_key": "ANTHROPIC_API_KEY",
            "api_website": "https://console.anthropic.com/",
            "default_model": "claude-3-haiku",
            "class_name": "ChatAnthropic",
            "env_var": "ANTHROPIC_API_KEY"
        },
        "Ollama (Local)": {
            "package": "langchain_community",
            "models": ["llama3.1:8b", "llama3", "mistral", "codellama", "phi3", "tinyllama"],
            "requires_api_key": False,
            "help_text": "Run locally using Ollama (no cloud API key required)",
            "icon": "🦙",
            "secret_key": None,
            "free": True,
            "default_model": "llama3.1:8b",
            "class_name": "ChatOllama",
            "env_var": None
        }
    }

    @classmethod
    def get_default_provider(cls) -> str:
        return "Groq"

    @classmethod
    def get_provider_info(cls, name: str) -> Dict[str, Any]:
        return cls.PROVIDERS.get(name, {})

    @classmethod
    def get_available_providers(cls) -> List[str]:
        return list(cls.PROVIDERS.keys())

# ==================== ERROR HANDLING CLASS ====================
class LLMError(Exception):
    """Custom exception for LLM errors"""
    def __init__(self, message: str, provider: str = None, error_type: str = None):
        self.message = message
        self.provider = provider
        self.error_type = error_type
        super().__init__(self.message)

# ==================== API ERROR DETECTION ====================
def detect_api_error(exception: Exception, provider: str) -> str:
    """
    Detect specific API errors and return user-friendly messages.
    """
    error_msg = str(exception).lower()
    
    # OpenAI specific errors
    if provider == "OpenAI":
        if "insufficient_quota" in error_msg or "quota" in error_msg:
            return "❌ OpenAI API quota exceeded. Please check your billing or upgrade plan at https://platform.openai.com/account/billing"
        elif "invalid_api_key" in error_msg:
            return "❌ Invalid OpenAI API key. Please check your key at https://platform.openai.com/api-keys"
        elif "rate_limit" in error_msg:
            return "⚠️ OpenAI rate limit exceeded. Please wait a moment and try again."
        elif "billing" in error_msg:
            return "❌ Billing issue with OpenAI. Please check your account billing."
    
    # Groq specific errors
    elif provider == "Groq":
        if "invalid_api_key" in error_msg or "authentication" in error_msg:
            return "❌ Invalid Groq API key. Get a free key from https://console.groq.com/keys"
        elif "rate_limit" in error_msg:
            return "⚠️ Groq rate limit exceeded. Free tier has limits. Try again later or upgrade."
        elif "quota" in error_msg:
            return "❌ Groq quota exceeded. Check usage at https://console.groq.com/usage"
    
    # Google Gemini specific errors
    elif provider == "Google Gemini":
        if "quota" in error_msg:
            return "❌ Google Gemini quota exceeded. Check usage at https://makersuite.google.com/app/apikey"
        elif "api_key_not_valid" in error_msg:
            return "❌ Invalid Google API key. Get one from https://makersuite.google.com/app/apikey"
    
    # Anthropic specific errors
    elif provider == "Anthropic Claude":
        if "invalid_api_key" in error_msg:
            return "❌ Invalid Anthropic API key. Get one from https://console.anthropic.com/"
        elif "quota" in error_msg:
            return "❌ Anthropic API quota exceeded. Check your account limits."
    
    # General API errors
    if "timeout" in error_msg:
        return "⏰ Request timeout. The API is taking too long to respond."
    elif "connection" in error_msg or "network" in error_msg:
        return "🌐 Network connection error. Please check your internet."
    elif "ssl" in error_msg:
        return "🔒 SSL certificate error. This might be a system issue."
    
    # Return generic error with provider info
    return f"❌ {provider} API Error: {str(exception)[:200]}"

# ==================== SAFE IMPORT HELPER ====================
def safe_import(module_path: str, class_name: str = None, silent: bool = False):
    """
    Safely import a module or class with detailed error handling.
    """
    try:
        if class_name:
            # Import specific class
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            if not silent:
                logger.debug(f"✅ Successfully imported {module_path}.{class_name}")
            return cls
        else:
            # Import module
            module = __import__(module_path)
            if not silent:
                logger.debug(f"✅ Successfully imported {module_path}")
            return module
    except ImportError as e:
        if not silent:
            logger.warning(f"⚠️ Failed to import {module_path}.{class_name if class_name else ''}: {e}")
        return None
    except Exception as e:
        if not silent:
            logger.error(f"❌ Unexpected error importing {module_path}: {e}")
        return None

# ==================== LLM CREATION FUNCTIONS WITH ERROR HANDLING ====================
def create_groq_llm(api_key: str, model: str, temperature: float):
    """Create Groq LLM instance with proper error handling"""
    try:
        if not api_key:
            raise LLMError("API key is required for Groq", "Groq", "missing_api_key")
        
        # Try different import paths
        ChatGroq = safe_import("langchain_groq", "ChatGroq")
        if not ChatGroq:
            ChatGroq = safe_import("langchain_groq.chat_models", "ChatGroq")
        
        if not ChatGroq:
            raise ImportError("langchain-groq package not found")
        
        # Create instance
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=temperature,
            streaming=True,
            max_retries=2,
            timeout=30
        )
        
        logger.info(f"✅ Groq LLM created: model={model}")
        return llm
        
    except ImportError as e:
        error_msg = f"❌ Groq package not installed. Install with: `pip install langchain-groq`"
        st.error(error_msg)
        logger.error(error_msg)
        return None
    except Exception as e:
        error_msg = detect_api_error(e, "Groq")
        st.error(error_msg)
        logger.error(f"Groq creation error: {e}")
        return None

def create_openai_llm(api_key: str, model: str, temperature: float):
    """Create OpenAI LLM instance with proper error handling"""
    try:
        if not api_key:
            raise LLMError("API key is required for OpenAI", "OpenAI", "missing_api_key")
        
        # Try different import paths
        ChatOpenAI = safe_import("langchain_openai", "ChatOpenAI")
        if not ChatOpenAI:
            ChatOpenAI = safe_import("langchain.chat_models", "ChatOpenAI")
        
        if not ChatOpenAI:
            raise ImportError("langchain-openai package not found")
        
        # Create instance
        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            streaming=True,
            max_retries=2,
            request_timeout=30
        )
        
        logger.info(f"✅ OpenAI LLM created: model={model}")
        return llm
        
    except ImportError as e:
        error_msg = f"❌ OpenAI package not installed. Install with: `pip install langchain-openai`"
        st.error(error_msg)
        logger.error(error_msg)
        return None
    except Exception as e:
        error_msg = detect_api_error(e, "OpenAI")
        st.error(error_msg)
        logger.error(f"OpenAI creation error: {e}")
        return None

def create_gemini_llm(api_key: str, model: str, temperature: float):
    """Create Google Gemini LLM instance with proper error handling"""
    try:
        if not api_key:
            raise LLMError("API key is required for Google Gemini", "Google Gemini", "missing_api_key")
        
        ChatGoogle = safe_import("langchain_google_genai", "ChatGoogleGenerativeAI")
        
        if not ChatGoogle:
            raise ImportError("langchain-google-genai package not found")
        
        # Create instance
        llm = ChatGoogle(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            streaming=True
        )
        
        logger.info(f"✅ Google Gemini LLM created: model={model}")
        return llm
        
    except ImportError as e:
        error_msg = f"❌ Google Gemini package not installed. Install with: `pip install langchain-google-genai google-generativeai`"
        st.error(error_msg)
        logger.error(error_msg)
        return None
    except Exception as e:
        error_msg = detect_api_error(e, "Google Gemini")
        st.error(error_msg)
        logger.error(f"Google Gemini creation error: {e}")
        return None

def create_anthropic_llm(api_key: str, model: str, temperature: float):
    """Create Anthropic LLM instance with proper error handling"""
    try:
        if not api_key:
            raise LLMError("API key is required for Anthropic", "Anthropic Claude", "missing_api_key")
        
        ChatAnthropic = safe_import("langchain_anthropic", "ChatAnthropic")
        
        if not ChatAnthropic:
            raise ImportError("langchain-anthropic package not found")
        
        # Create instance
        llm = ChatAnthropic(
            anthropic_api_key=api_key,
            model=model,
            temperature=temperature,
            streaming=True,
            max_tokens=1024
        )
        
        logger.info(f"✅ Anthropic LLM created: model={model}")
        return llm
        
    except ImportError as e:
        error_msg = f"❌ Anthropic package not installed. Install with: `pip install langchain-anthropic anthropic`"
        st.error(error_msg)
        logger.error(error_msg)
        return None
    except Exception as e:
        error_msg = detect_api_error(e, "Anthropic Claude")
        st.error(error_msg)
        logger.error(f"Anthropic creation error: {e}")
        return None

def create_ollama_llm(model: str, temperature: float, base_url: str = "http://localhost:11434"):
    """Create Ollama LLM instance with proper error handling"""
    try:
        ChatOllama = safe_import("langchain_community.chat_models", "ChatOllama")
        
        if not ChatOllama:
            raise ImportError("langchain-community package not found")
        
        # Test connection first
        import requests
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                st.warning(f"⚠️ Ollama server at {base_url} responded with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.warning(f"⚠️ Cannot connect to Ollama at {base_url}. Make sure Ollama is running.")
        
        # Create instance
        llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature,
            timeout=60
        )
        
        logger.info(f"✅ Ollama LLM created: model={model}, url={base_url}")
        return llm
        
    except ImportError as e:
        error_msg = f"❌ Ollama package not installed. Install with: `pip install langchain-community ollama`"
        st.error(error_msg)
        logger.error(error_msg)
        return None
    except Exception as e:
        error_msg = f"❌ Ollama Error: {str(e)[:200]}"
        st.error(error_msg)
        logger.error(f"Ollama creation error: {e}")
        return None

# ==================== TEST CONNECTION FUNCTIONS ====================
def test_api_connection(provider: str, api_key: str = None, model: str = None):
    """
    Test API connection with a simple request.
    Returns (success, message)
    """
    try:
        import requests

        # -------------------- GROQ --------------------
        if provider == "Groq":
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json={
                    "model": model or "llama3-8b-8192",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10
                },
                timeout=10
            )
            if response.status_code == 200:
                return True, "✅ Groq API connection successful"
            else:
                return False, f"❌ Groq API error: {response.status_code} - {response.text[:100]}"

        # -------------------- OPENAI --------------------
        elif provider == "OpenAI":
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, "✅ OpenAI API connection successful"
            else:
                return False, f"❌ OpenAI API error: {response.status_code} - {response.text[:100]}"

        # -------------------- GOOGLE GEMINI --------------------
        elif provider == "Google Gemini":
            model_name = model or "gemini-pro"
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent",
                params={"key": api_key},
                json={
                    "contents": [
                        {"parts": [{"text": "Hello"}]}
                    ]
                },
                timeout=10
            )
            if response.status_code == 200:
                return True, "✅ Google Gemini API connection successful"
            else:
                return False, f"❌ Google Gemini API error: {response.status_code} - {response.text[:100]}"

        # -------------------- ANTHROPIC CLAUDE --------------------
        elif provider == "Anthropic Claude":
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json={
                    "model": model or "claude-3-haiku",
                    "max_tokens": 10,
                    "messages": [
                        {"role": "user", "content": "Hello"}
                    ]
                },
                timeout=10
            )
            if response.status_code == 200:
                return True, "✅ Anthropic Claude API connection successful"
            else:
                return False, f"❌ Anthropic API error: {response.status_code} - {response.text[:100]}"

        # -------------------- FALLBACK --------------------
        return False, f"❌ Test not implemented for {provider}"

    except Exception as e:
        return False, f"❌ Connection test failed: {str(e)[:200]}"

# ==================== MAIN LLM CREATOR ====================
def create_llm_instance(config: Dict[str, Any]):
    """
    Create and return a chat model instance based on configuration.
    """
    if not config:
        st.error("❌ No configuration provided")
        return None
    
    provider = config.get("provider", "Groq")
    api_key = config.get("api_key", "")
    model = config.get("model", "")
    temperature = config.get("temperature", 0.7)
    
    logger.info(f"Creating LLM instance: provider={provider}, model={model}")
    
    # Get provider info
    provider_info = ProviderConfig.get_provider_info(provider)
    if not provider_info:
        st.error(f"❌ Unknown provider: {provider}")
        return None
    
    # Set default model if not specified
    if not model:
        model = provider_info.get("default_model", "")
    
    # Check API key for cloud providers
    if provider_info.get("requires_api_key") and not api_key:
        # Try to get from environment
        env_var = provider_info.get("env_var")
        if env_var:
            api_key = os.environ.get(env_var, "")
        
        # Try to get from secrets
        if not api_key:
            secret_key = provider_info.get("secret_key")
            if secret_key:
                api_key = st.secrets.get(secret_key, "")
        
        if not api_key:
            st.error(f"❌ API key required for {provider}. Please enter it in the sidebar.")
            return None
    
    # Create LLM based on provider
    with st.spinner(f"Configuring {provider}..."):
        if provider == "Groq":
            return create_groq_llm(api_key, model, temperature)
        
        elif provider == "OpenAI":
            return create_openai_llm(api_key, model, temperature)
        
        elif provider == "Google Gemini":
            return create_gemini_llm(api_key, model, temperature)
        
        elif provider == "Anthropic Claude":
            return create_anthropic_llm(api_key, model, temperature)
        
        elif provider == "Ollama (Local)":
            base_url = config.get("base_url", "http://localhost:11434")
            return create_ollama_llm(model, temperature, base_url)
        
        else:
            st.error(f"❌ Unsupported provider: {provider}")
            return None

# ==================== SIDEBAR CONFIGURATION ====================
def configure_llm_sidebar(show_test_button: bool = True):
    """Set up the provider selection UI in Streamlit sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.subheader("🤖 AI Configuration")
        
        # Get available providers
        providers = ProviderConfig.get_available_providers()
        default_provider = ProviderConfig.get_default_provider()
        
        # Ensure Groq is first
        if default_provider in providers:
            providers.remove(default_provider)
            providers.insert(0, default_provider)
        
        # Provider selection
        selected_provider = st.selectbox(
            "Select AI Provider",
            options=providers,
            index=0,
            key="llm_provider",
            help="Choose your AI provider. Groq is recommended for best performance."
        )
        
        # Provider info
        provider_info = ProviderConfig.get_provider_info(selected_provider)
        
        # Display provider info
        st.markdown(f"**{provider_info.get('icon', '')} {selected_provider}**")
        st.caption(provider_info.get("help_text", ""))
        
        # API Key input (if required)
        api_key = ""
        if provider_info.get("requires_api_key"):
            secret_key = provider_info.get("secret_key")
            env_var = provider_info.get("env_var")
            
            # Try to get from environment first
            env_key = os.environ.get(env_var, "") if env_var else ""
            
            # Try to get from secrets
            secret_value = st.secrets.get(secret_key, "") if secret_key else ""
            
            # Use environment variable if available, else secrets, else empty
            default_key = env_key if env_key else secret_value
            
            api_key = st.text_input(
                f"{selected_provider} API Key",
                value=default_key,
                type="password",
                placeholder=f"Enter {selected_provider} API key",
                help=f"Get from {provider_info.get('api_website', '')}",
                key=f"{selected_provider.lower().replace(' ', '_')}_api_key"
            )
            
            if not api_key and not default_key:
                st.warning(f"⚠️ {selected_provider} API key is required for this provider")
                
                # Show quick link to get API key
                api_website = provider_info.get("api_website", "")
                if api_website:
                    st.markdown(f"[🔑 Get {selected_provider} API Key]({api_website})")
        
        else:
            st.info("🎉 No API key required - runs locally")
        
        # Model selection
        model_options = provider_info.get("models", [])
        default_model = provider_info.get("default_model", model_options[0] if model_options else "")
        
        model = st.selectbox(
            "Select Model",
            options=model_options,
            index=model_options.index(default_model) if default_model in model_options else 0,
            key=f"{selected_provider.lower().replace(' ', '_')}_model"
        )
        
        # Temperature slider
        temperature = st.slider(
            "Creativity (temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            key=f"{selected_provider.lower().replace(' ', '_')}_temperature",
            help="Lower = more focused, Higher = more creative"
        )
        
        # Extra configurations
        extra_config = {}
        
        # Test API Connection button
        if show_test_button and provider_info.get("requires_api_key") and api_key:
            if st.button("🔍 Test API Connection", key="test_api_connection", use_container_width=True):
                with st.spinner("Testing connection..."):
                    success, message = test_api_connection(selected_provider, api_key, model)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        # Ollama-specific settings
        if selected_provider == "Ollama (Local)":
            base_url = st.text_input(
                "Ollama Server URL",
                value="http://localhost:11434",
                help="Change if Ollama runs on a different host/port",
                key="ollama_base_url"
            )
            extra_config["base_url"] = base_url
            
            # Test connection button
            if st.button("🚀 Test Ollama Connection", key="test_ollama", use_container_width=True):
                try:
                    import requests
                    with st.spinner("Connecting to Ollama..."):
                        response = requests.get(f"{base_url}/api/tags", timeout=5)
                        if response.status_code == 200:
                            models = response.json().get("models", [])
                            if models:
                                model_names = [m.get('name', '') for m in models[:5]]
                                st.success(f"✅ Ollama is running. Available models: {', '.join(model_names)}")
                            else:
                                st.success("✅ Ollama is running but no models found.")
                        else:
                            st.error("❌ Ollama responded but not OK")
                except Exception as e:
                    st.error(f"❌ Cannot reach Ollama: {e}")
                    st.info("Make sure Ollama is installed and running: `ollama serve`")
        
        # Build configuration dictionary
        config = {
            "provider": selected_provider,
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            **extra_config
        }
        
        # Installation status
        with st.expander("📦 Installation Status", expanded=False):
            packages = {
                "Groq": ["langchain_groq"],
                "OpenAI": ["langchain_openai"],
                "Google Gemini": ["langchain_google_genai", "google.generativeai"],
                "Anthropic Claude": ["langchain_anthropic"],
                "Ollama (Local)": ["langchain_community", "ollama"]
            }
            
            if selected_provider in packages:
                for package in packages[selected_provider]:
                    try:
                        __import__(package)
                        st.success(f"✅ {package}")
                    except ImportError:
                        st.error(f"❌ {package} (not installed)")
        
        return config

# ==================== UTILITY FUNCTIONS ====================
def get_llm_from_config(config: Dict[str, Any]):
    """Create LLM instance from configuration"""
    return create_llm_instance(config)

def provider_selection_sidebar():
    """Legacy compatibility function"""
    return configure_llm_sidebar()

def get_configured_llm():
    """Get configured LLM directly"""
    config = configure_llm_sidebar()
    return get_llm_from_config(config)

# ==================== RESPONSE EXTRACTION ====================
def extract_response(response):
    """
    Extract text from various LLM response formats.
    """
    if response is None:
        return "No response received"
    
    # If response has content attribute
    if hasattr(response, 'content'):
        content = response.content
        if content is not None:
            return str(content)
    
    # If response has text attribute
    if hasattr(response, 'text'):
        text = response.text
        if text is not None:
            return str(text)
    
    # If response is a string
    if isinstance(response, str):
        return response
    
    # If response is a dict
    if isinstance(response, dict):
        # Try common keys
        for key in ['content', 'text', 'response', 'output', 'answer', 'result', 'message']:
            if key in response and response[key]:
                return str(response[key])
        
        # OpenAI format
        if 'choices' in response and isinstance(response['choices'], list) and len(response['choices']) > 0:
            choice = response['choices'][0]
            if isinstance(choice, dict):
                if 'message' in choice and isinstance(choice['message'], dict):
                    return str(choice['message'].get('content', ''))
                elif 'text' in choice:
                    return str(choice['text'])
    
    # If response has generations attribute (LangChain)
    if hasattr(response, 'generations'):
        try:
            generations = response.generations
            if generations and len(generations) > 0:
                first_gen = generations[0]
                if first_gen and len(first_gen) > 0:
                    return str(first_gen[0].text)
        except:
            pass
    
    # Fallback: convert to string
    return str(response)

def invoke_llm(llm, prompt: str, callbacks=None):
    """
    Safely invoke LLM with different calling patterns and proper error handling.
    """
    if llm is None:
        return "❌ LLM not configured. Please check sidebar settings."
    
    try:
        # Try invoke method (most common)
        if hasattr(llm, 'invoke'):
            try:
                response = llm.invoke(prompt, callbacks=callbacks) if callbacks else llm.invoke(prompt)
                return extract_response(response)
            except Exception as e:
                logger.error(f"invoke() failed: {e}")
                # Continue to try other methods
        
        # Try generate method
        if hasattr(llm, 'generate'):
            try:
                response = llm.generate([prompt])
                return extract_response(response)
            except Exception as e:
                logger.error(f"generate() failed: {e}")
                # Continue to try other methods
        
        # Try __call__ method
        if callable(llm):
            try:
                response = llm(prompt)
                return extract_response(response)
            except Exception as e:
                logger.error(f"__call__() failed: {e}")
        
        # If all methods failed
        error_msg = f"❌ Could not invoke LLM. The LLM object doesn't have a compatible interface."
        logger.error(error_msg)
        return error_msg
        
    except Exception as e:
        # Get provider name from llm if possible
        provider = "Unknown"
        if hasattr(llm, '__class__'):
            class_name = llm.__class__.__name__
            if 'Groq' in class_name:
                provider = "Groq"
            elif 'OpenAI' in class_name:
                provider = "OpenAI"
            elif 'Google' in class_name:
                provider = "Google Gemini"
            elif 'Anthropic' in class_name:
                provider = "Anthropic Claude"
            elif 'Ollama' in class_name:
                provider = "Ollama"
        
        error_msg = detect_api_error(e, provider)
        logger.error(f"LLM invocation error ({provider}): {e}")
        return error_msg

