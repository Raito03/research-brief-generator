# Graceful shutdown and lifespan management
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from fastapi import FastAPI

logger = logging.getLogger("api")


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
