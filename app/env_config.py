# Environment validation for production
import os
from typing import List, Optional


class EnvironmentError(Exception):
    """Raised when required environment variables are missing"""

    pass


def validate_environment() -> List[str]:
    """
    Validate required environment variables on startup.
    Returns list of configured providers.
    """
    missing = []
    providers = []

    # Check each provider - at least one must be configured
    if os.getenv("GOOGLE_API_KEY"):
        providers.append("google")
    if os.getenv("CF_ACCOUNT_ID") and os.getenv("CF_API_TOKEN"):
        providers.append("cloudflare")
    if os.getenv("OPENROUTER_API_KEY"):
        providers.append("openrouter")

    if not providers:
        missing.append(
            "No LLM provider configured (GOOGLE_API_KEY, CF_* + CF_*, or OPENROUTER_API_KEY)"
        )

    return providers


def get_required_env_vars() -> dict:
    """
    Get environment variables with their descriptions.
    """
    return {
        "GOOGLE_API_KEY": "Google AI Studio API key (primary provider)",
        "CF_ACCOUNT_ID": "Cloudflare Account ID (fallback provider)",
        "CF_API_TOKEN": "Cloudflare API Token (fallback provider)",
        "OPENROUTER_API_KEY": "OpenRouter API key (backup provider)",
        "API_CORS_ORIGINS": "Comma-separated CORS origins",
    }


def check_env_var(name: str, required: bool = False) -> Optional[str]:
    """
    Get environment variable with optional validation.
    """
    value = os.getenv(name)
    if required and not value:
        raise EnvironmentError(f"Required environment variable {name} is not set")
    return value
