import logging
import streamlit as st

logger = logging.getLogger("streaming")
logger.setLevel(logging.INFO)

BaseCallbackHandler = None
_import_errors = []

try:
    from langchain_core.callbacks import BaseCallbackHandler  # type: ignore[import]
    BaseCallbackHandler = BaseCallbackHandler
except Exception as e:
    _import_errors.append(f"langchain_core.callbacks: {e}")
    try:
        from langchain.callbacks.base import BaseCallbackHandler  # type: ignore[import]
        BaseCallbackHandler = BaseCallbackHandler
    except Exception as e2:
        _import_errors.append(f"langchain.callbacks.base: {e2}")
        try:
            from langchain_community.callbacks import BaseCallbackHandler  # type: ignore[import]# type: ignore[import]
            BaseCallbackHandler = BaseCallbackHandler
        except Exception as e3:
            _import_errors.append(f"langchain_community.callbacks: {e3}")

# If nothing worked, provide a minimal fallback so imports don't fail.
if BaseCallbackHandler is None:
    class BaseCallbackHandler:
        """
        Minimal fallback BaseCallbackHandler.
        This only implements the method used in the UI streaming handler (on_llm_new_token).
        It is NOT a full replacement for the real class - install langchain or langchain_core
        for full features.
        """
        def __init__(self):
            pass

        def on_llm_new_token(self, token: str, **kwargs) -> None:
            # fallback: do nothing, keep compatibility
            return None

        def on_llm_end(self, **kwargs) -> None:
            return None

# StreamHandler uses the BaseCallbackHandler interface
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text: str = ""):
        try:
            super().__init__()  # call parent if present
        except Exception:
            pass
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        # Append token and update the Streamlit placeholder
        try:
            self.text += token
            # Update container:
            try:
                self.container.markdown(self.text)
            except Exception:
                # Some callbacks call very fast; ignore render errors gracefully
                pass
        except Exception:
            logger.exception("Error in StreamHandler.on_llm_new_token")

    def on_llm_end(self, **kwargs):
        pass