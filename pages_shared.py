import logging
from typing import Any, Optional
import traceback

logger = logging.getLogger(__name__)

def extract_text(obj: Any) -> str:
    if obj is None:
        return ""
    
    # Direct string
    if isinstance(obj, str):
        return obj
    
    # Object with content attribute
    if hasattr(obj, "content"):
        try:
            content = getattr(obj, "content")
            if content is not None:
                return str(content)
        except:
            pass
    
    # Object with text attribute
    if hasattr(obj, "text"):
        try:
            text = getattr(obj, "text")
            if text is not None:
                return str(text)
        except:
            pass
    
    # Dictionary
    if isinstance(obj, dict):
        # Try common response keys
        for key in ["text", "content", "response", "output", "answer", "result", "message"]:
            if key in obj and obj[key] is not None:
                return str(obj[key])
        
        # Try nested content in choices (OpenAI format)
        if "choices" in obj and isinstance(obj["choices"], list) and len(obj["choices"]) > 0:
            choice = obj["choices"][0]
            if isinstance(choice, dict):
                if "message" in choice and isinstance(choice["message"], dict):
                    return str(choice["message"].get("content", ""))
                elif "text" in choice:
                    return str(choice["text"])
        
        # Try error messages
        if "error" in obj and isinstance(obj["error"], dict):
            error_msg = obj["error"].get("message", "")
            if error_msg:
                return f"❌ API Error: {error_msg}"
    
    # LangChain generations format
    if hasattr(obj, "generations"):
        try:
            gens = getattr(obj, "generations")
            if isinstance(gens, list) and len(gens) > 0:
                first_gen = gens[0]
                if isinstance(first_gen, list) and len(first_gen) > 0:
                    candidate = first_gen[0]
                    if hasattr(candidate, "text"):
                        text = getattr(candidate, "text", "")
                        if text:
                            return str(text)
                    if hasattr(candidate, "content"):
                        content = getattr(candidate, "content", "")
                        if content:
                            return str(content)
        except Exception as e:
            logger.debug(f"Error extracting from generations: {e}")
    
    # Try to get string representation
    try:
        str_repr = str(obj)
        if str_repr and str_repr != "None":
            # Check if it looks like an error
            if any(err in str_repr.lower() for err in ["error", "exception", "failed", "invalid", "quota", "limit"]):
                return f"❌ {str_repr[:200]}"
            return str_repr
    except:
        pass
    
    return ""

def llm_invoke(llm: Any, prompt: str, callbacks: list = None, provider_name: str = None) -> str:
    """
    Universal LLM invocation with comprehensive error handling.
    Returns meaningful error messages for users.
    """
    if llm is None:
        return "❌ LLM not configured. Please:\n1. Select a provider in sidebar\n2. Enter API key if required\n3. Try again"
    
    methods_to_try = []
    
    if hasattr(llm, "invoke"):
        methods_to_try.append(("invoke", lambda: llm.invoke(prompt, callbacks=callbacks) if callbacks else llm.invoke(prompt)))
    
    if hasattr(llm, "generate"):
        methods_to_try.append(("generate", lambda: llm.generate([prompt])))
    
    if hasattr(llm, "chat"):
        methods_to_try.append(("chat", lambda: llm.chat(prompt)))
    
    if callable(llm):
        methods_to_try.append(("__call__", lambda: llm(prompt)))
    
    last_error = None
    for method_name, method_func in methods_to_try:
        try:
            logger.debug(f"Trying {method_name}() method")
            result = method_func()
            extracted = extract_text(result)
            
            if extracted and extracted.strip():
                # Check if it's an error message
                if extracted.startswith("❌"):
                    return extracted
                return extracted
            
        except Exception as e:
            last_error = e
            logger.debug(f"Method {method_name} failed: {str(e)[:100]}")
            continue
    
    # If all methods failed, provide helpful error message
    if last_error:
        error_str = str(last_error).lower()
        
        # Provide specific guidance based on error
        if "api" in error_str and "key" in error_str:
            return "❌ Invalid API key. Please check your API key in the sidebar."
        elif "quota" in error_str:
            return "❌ API quota exceeded. Please check your account limits or try a different provider."
        elif "rate" in error_str and "limit" in error_str:
            return "⚠️ Rate limit exceeded. Please wait a moment and try again."
        elif "connection" in error_str or "timeout" in error_str:
            return "🌐 Connection error. Please check your internet connection."
        elif provider_name:
            return f"❌ {provider_name} Error: {str(last_error)[:150]}"
        else:
            return f"❌ API Error: {str(last_error)[:150]}"
    
    # If no specific error but still failed
    return "❌ Could not get response. Please:\n1. Check API key is valid\n2. Check provider status\n3. Try a different model\n4. Contact support if issue persists"

def format_chat_message(role: str, content: str) -> dict:
    """
    Format chat message for session state.
    """
    return {"role": role, "content": content}

def get_provider_display_name(provider: str) -> str:
    """
    Get friendly display name for provider.
    """
    display_names = {
        "Groq": "⚡ Groq",
        "OpenAI": "🔑 OpenAI",
        "Google Gemini": "🌐 Google Gemini",
        "Anthropic Claude": "🧠 Anthropic Claude",
        "Ollama (Local)": "🦙 Ollama (Local)"
    }
    return display_names.get(provider, provider)

def get_provider_troubleshooting(provider: str) -> str:
    tips = {
        "Groq": """
        **Groq Troubleshooting:**
        1. Get a free API key from: https://console.groq.com/keys
        2. Free tier has rate limits (30 RPM, 10k TPM)
        3. Check usage: https://console.groq.com/usage
        4. Install: `pip install langchain-groq`
        """,
        "OpenAI": """
        **OpenAI Troubleshooting:**
        1. Get API key: https://platform.openai.com/api-keys
        2. Check billing: https://platform.openai.com/account/billing
        3. Free trial may be expired
        4. Install: `pip install langchain-openai`
        """,
        "Google Gemini": """
        **Google Gemini Troubleshooting:**
        1. Get API key: https://makersuite.google.com/app/apikey
        2. Enable Gemini API in Google Cloud Console
        3. Check quota: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
        4. Install: `pip install langchain-google-genai google-generativeai`
        """,
        "Anthropic Claude": """
        **Anthropic Claude Troubleshooting:**
        1. Get API key: https://console.anthropic.com/
        2. Check usage limits
        3. Install: `pip install langchain-anthropic anthropic`
        """,
        "Ollama (Local)": """
        **Ollama Troubleshooting:**
        1. Install Ollama: https://ollama.ai
        2. Run: `ollama serve`
        3. Pull model: `ollama pull llama3`
        4. Install: `pip install langchain-community ollama`
        """
    }
    return tips.get(provider, "Check provider documentation for troubleshooting.")