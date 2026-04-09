import os
from contextvars import ContextVar
from typing import Any, Callable, List, Optional

from google.api_core.exceptions import ResourceExhausted
from langchain_core.language_models.chat_models import SimpleChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import ConfigDict


request_log_callback: ContextVar[Optional[Callable]] = ContextVar(
    "request_log_callback", default=None
)
model_name_ctx: ContextVar[Optional[str]] = ContextVar("model_name_ctx", default=None)


def set_log_callback(callback: Callable):
    """Set callback function for streaming logs"""
    request_log_callback.set(callback)


def stream_log(message: str):
    """Send log message to callback and print to console"""
    print(message)  # Always print to console

    cb = request_log_callback.get()
    if cb:
        try:
            cb(message)
        except:
            pass  # Don't break workflow if callback fails


class CloudflareChatWrapper(SimpleChatModel):
    """
    Wrapper to make CloudflareWorkersAI compatible with Chat interface
    Properly configured for Pydantic v2
    """

    # ✅ Use ConfigDict for Pydantic v2
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Allow CloudflareWorkersAI type
        extra="allow",  # Allow extra fields
    )

    # ✅ Define fields properly
    account_id: str
    api_token: str
    model_name: str = "@cf/meta/llama-3.1-8b-instruct"
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    # Internal LLM instance (initialized after __init__)
    _llm: Any = None

    def __init__(self, **data):
        """Initialize the wrapper and create CloudflareWorkersAI instance"""
        super().__init__(**data)

        # Create the actual Cloudflare LLM after initialization
        from langchain_community.llms.cloudflare_workersai import CloudflareWorkersAI

        self._llm = CloudflareWorkersAI(
            account_id=self.account_id,
            api_token=self.api_token,
            model=self.model_name,
            streaming=False,
        )

    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        """
        Convert messages to prompt and call CloudflareWorkersAI
        """
        # Convert messages to a single string prompt
        prompt = "\n".join(
            [
                f"{'User' if msg.type == 'human' else 'Assistant'}: {msg.content}"
                for msg in messages
            ]
        )

        # Call the LLM (returns string)
        response = self._llm.invoke(prompt)

        return response

    @property
    def _llm_type(self) -> str:
        """Return identifier for this model"""
        return "cloudflare-chat-wrapper"


def create_openrouter_llm(temperature: float = 0, max_tokens: int = 2000) -> ChatOpenAI:
    """
    Create LLM with multi-provider fallback strategy
    Priority: Google AI Studio (Gemini) → Cloudflare Workers AI → OpenRouter
    """
    # Provider configurations with their models
    providers = [
        {
            "name": "Google Gemini",
            "type": "google",
            "model": "gemini-2.0-flash-lite",
            "api_key_env": "GOOGLE_API_KEY",
        },
        {
            "name": "Cloudflare Workers AI",
            "type": "cloudflare",
            "model": "@cf/meta/llama-3.1-8b-instruct",
            "account_id_env": "CF_ACCOUNT_ID",
            "api_token_env": "CF_API_TOKEN",
        },
        {
            "name": "OpenRouter (DeepSeek)",
            "type": "openrouter",
            "model": "deepseek/deepseek-chat-v3.1:free",
            "api_key_env": "OPENROUTER_API_KEY",
        },
    ]

    for provider in providers:
        try:
            if provider["type"] == "google":
                # Google AI Studio / Gemini
                from langchain_google_genai import ChatGoogleGenerativeAI

                api_key = os.getenv(provider["api_key_env"])
                if not api_key:
                    stream_log(f"⚠️  {provider['name']}: API key not found, skipping...")
                    continue

                llm = ChatGoogleGenerativeAI(
                    model=provider["model"],
                    google_api_key=api_key,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    max_retries=0,
                    request_timeout=30,  # ✅ 30 second timeout
                    streaming=True,
                )

                # Test the connection with quota error handling
                try:
                    test_response = llm.invoke([HumanMessage(content="test")])
                    model_name_ctx.set(provider["name"])
                    stream_log(
                        f"✅ Successfully connected to {provider['name']} ({provider['model']})"
                    )
                    return llm
                except ResourceExhausted as quota_error:
                    # ✅ INSTANT SWITCH on quota exhaustion
                    stream_log(
                        f"❌ {provider['name']}: Quota exhausted - switching to next provider immediately"
                    )
                    stream_log(f"   Error: {str(quota_error)[:100]}...")
                    continue  # Skip to next provider immediately

            elif provider["type"] == "cloudflare":
                # Cloudflare Workers AI

                account_id = os.getenv(provider["account_id_env"])
                api_token = os.getenv(provider["api_token_env"])

                if not account_id or not api_token:
                    stream_log(
                        f"⚠️  {provider['name']}: Credentials not found, skipping..."
                    )
                    continue

                llm = CloudflareChatWrapper(
                    account_id=account_id,
                    api_token=api_token,
                    model=provider["model"],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # Test the connection
                test_response = llm.invoke([HumanMessage(content="test")])
                model_name_ctx.set(provider["name"])
                stream_log(
                    f"✅ Successfully connected to {provider['name']} ({provider['model']})"
                )
                return llm

            elif provider["type"] == "openrouter":
                # OpenRouter fallback (your existing implementation)
                api_key = os.getenv(provider["api_key_env"])
                if not api_key:
                    stream_log(f"⚠️  {provider['name']}: API key not found, skipping...")
                    continue

                llm = ChatOpenAI(
                    model=provider["model"],
                    openai_api_key=api_key,
                    openai_api_base="https://openrouter.ai/api/v1",
                    temperature=temperature,
                    max_tokens=max_tokens,
                    default_headers={
                        "HTTP-Referer": "http://localhost:5000",
                        "X-Title": "Research Brief Generator",
                    },
                    streaming=True,
                )

                model_name_ctx.set(provider["name"])
                stream_log(
                    f"✅ Successfully connected to {provider['name']} ({provider['model']})"
                )
                return llm

        except ResourceExhausted as quota_error:
            # Catch quota errors at the provider level
            stream_log(
                f"❌ {provider['name']}: Quota exhausted - switching immediately"
            )
            continue

        except Exception as e:
            stream_log(f"❌ Failed to connect to {provider['name']}: {str(e)}")
            continue

    # If all providers fail
    stream_log("🚨 CRITICAL: All LLM providers failed or exhausted")
    raise RuntimeError(
        "❌ Failed to create LLM with all providers. "
        "Please check your API keys: GOOGLE_API_KEY, CF_ACCOUNT_ID, CF_API_TOKEN, OPENROUTER_API_KEY"
    )
