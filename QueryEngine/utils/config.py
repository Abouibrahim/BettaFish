"""
Query Engine configuration management module

This module uses pydantic-settings to manage Query Engine configuration, supporting automatic loading from environment variables and .env files.
Data model definition location:
- This file - Configuration model definition
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from loguru import logger


# Calculate .env priority: prioritize current working directory, then project root
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
CWD_ENV: Path = Path.cwd() / ".env"
ENV_FILE: str = str(CWD_ENV if CWD_ENV.exists() else (PROJECT_ROOT / ".env"))


class Settings(BaseSettings):
    """
    Query Engine global configuration; supports automatic loading of .env and environment variables.
    Variable names are consistent with original config.py uppercase for smooth transition.
    """

    # ======================= LLM Related =======================
    QUERY_ENGINE_API_KEY: str = Field(..., description="Query Engine LLM API key for main LLM. You can change the API used by each component's LLM. As long as it's compatible with OpenAI request format, you can use it normally by defining KEY, BASE_URL, and MODEL_NAME.")
    QUERY_ENGINE_BASE_URL: Optional[str] = Field(None, description="Query Engine LLM interface BaseUrl, can customize vendor API")
    QUERY_ENGINE_MODEL_NAME: str = Field(..., description="Query Engine LLM model name")
    QUERY_ENGINE_PROVIDER: Optional[str] = Field(None, description="Query Engine LLM provider (compatibility field)")

    # ================== Network Tools Configuration ====================
    TAVILY_API_KEY: str = Field(..., description="Tavily API (application address: https://www.tavily.com/) API key for Tavily web search")

    # ================== Search Parameters Configuration ====================
    SEARCH_TIMEOUT: int = Field(240, description="Search timeout (seconds)")
    SEARCH_CONTENT_MAX_LENGTH: int = Field(20000, description="Maximum content length for prompts")
    MAX_REFLECTIONS: int = Field(2, description="Maximum reflection rounds")
    MAX_PARAGRAPHS: int = Field(5, description="Maximum paragraphs")
    MAX_SEARCH_RESULTS: int = Field(20, description="Maximum search results")

    # ================== Output Configuration ====================
    OUTPUT_DIR: str = Field("reports", description="Output directory")
    SAVE_INTERMEDIATE_STATES: bool = Field(True, description="Whether to save intermediate states")
    
    class Config:
        env_file = ENV_FILE
        env_prefix = ""
        case_sensitive = False
        extra = "allow"


# Create global configuration instance
settings = Settings()

def print_config(config: Settings):
    """
    Print configuration information

    Args:
        config: Settings configuration object
    """
    message = ""
    message += "=== Query Engine Configuration ===\n"
    message += f"LLM Model: {config.QUERY_ENGINE_MODEL_NAME}\n"
    message += f"LLM Base URL: {config.QUERY_ENGINE_BASE_URL or '(default)'}\n"
    message += f"Tavily API Key: {'Configured' if config.TAVILY_API_KEY else 'Not configured'}\n"
    message += f"Search Timeout: {config.SEARCH_TIMEOUT} seconds\n"
    message += f"Max Content Length: {config.SEARCH_CONTENT_MAX_LENGTH}\n"
    message += f"Max Reflections: {config.MAX_REFLECTIONS}\n"
    message += f"Max Paragraphs: {config.MAX_PARAGRAPHS}\n"
    message += f"Max Search Results: {config.MAX_SEARCH_RESULTS}\n"
    message += f"Output Directory: {config.OUTPUT_DIR}\n"
    message += f"Save Intermediate States: {config.SAVE_INTERMEDIATE_STATES}\n"
    message += f"LLM API Key: {'Configured' if config.QUERY_ENGINE_API_KEY else 'Not configured'}\n"
    message += "===================================\n"
    logger.info(message)
