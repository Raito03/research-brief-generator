# Graceful shutdown and lifespan management
import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from fastapi import FastAPI

logger = logging.getLogger("api")

# Sentry error tracking - minimal setup
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            traces_sample_rate=0.1,  # 10% of transactions
            environment=os.getenv("RAILWAY_ENVIRONMENT", "production"),
        )
        logger.info("Sentry error tracking enabled")
    except Exception as e:
        logger.warning(f"Sentry initialization failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    Handles graceful startup and shutdown.
    """
    # Startup
    logger.info("Starting Research Brief Generator API...")

    # Validate environment
    try:
        from app.env_config import validate_environment

        providers = validate_environment()
        logger.info(f"Configured providers: {', '.join(providers)}")
    except Exception as e:
        logger.warning(f"Environment validation failed: {e}")

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down gracefully...")

    # Close any connections
    try:
        from app.llm_providers import reset_request_provider_config

        reset_request_provider_config()
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

    logger.info("Shutdown complete")
