# -*- coding: utf-8 -*-
"""
BettaFish Configuration File

This module uses pydantic-settings to manage global configuration, supporting automatic loading from environment variables and .env files.
Data model definition location:
- This file - Configuration model definitions
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional
from loguru import logger


# Calculate .env priority: prioritize current working directory, then project root directory
PROJECT_ROOT: Path = Path(__file__).resolve().parent
CWD_ENV: Path = Path.cwd() / ".env"
ENV_FILE: str = str(CWD_ENV if CWD_ENV.exists() else (PROJECT_ROOT / ".env"))


class Settings(BaseSettings):
    """
    Global configuration; supports automatic loading from .env and environment variables.
    Variable names match original config.py capitalization for smooth transition.
    """
    # ================== Flask Server Configuration ====================
    HOST: str = Field("0.0.0.0", description="BettaFish host address, e.g., 0.0.0.0 or 127.0.0.1")
    PORT: int = Field(5000, description="Flask server port number, default 5000")

    # ====================== Database Configuration ======================
    DB_DIALECT: str = Field("postgresql", description="Database type, options: mysql or postgresql; configure together with other connection information")
    DB_HOST: str = Field("your_db_host", description="Database host, e.g., localhost or 127.0.0.1")
    DB_PORT: int = Field(3306, description="Database port number, default 3306")
    DB_USER: str = Field("your_db_user", description="Database username")
    DB_PASSWORD: str = Field("your_db_password", description="Database password")
    DB_NAME: str = Field("your_db_name", description="Database name")
    DB_CHARSET: str = Field("utf8mb4", description="Database character set, utf8mb4 recommended for emoji compatibility")
    
    # ======================= LLM Configuration =======================
    # Our LLM model API sponsors: https://share.302.ai/P66Qe3, https://aihubmix.com/?aff=8Ds9, providing comprehensive model APIs
    
    # Insight Agent (Kimi recommended, application URL: https://platform.moonshot.cn/)
    INSIGHT_ENGINE_API_KEY: Optional[str] = Field(None, description="Insight Agent (kimi-k2 recommended, official application URL: https://platform.moonshot.cn/) API key for primary LLM. Please apply and test with recommended configuration first, then adjust KEY, BASE_URL, and MODEL_NAME as needed.")
    INSIGHT_ENGINE_BASE_URL: Optional[str] = Field("https://api.moonshot.cn/v1", description="Insight Agent LLM base URL, customizable by provider")
    INSIGHT_ENGINE_MODEL_NAME: str = Field("kimi-k2-0711-preview", description="Insight Agent LLM model name, e.g., kimi-k2-0711-preview")
    
    # Media Agent (Gemini recommended, relay provider recommended: https://aihubmix.com/?aff=8Ds9)
    MEDIA_ENGINE_API_KEY: Optional[str] = Field(None, description="Media Agent (gemini-2.5-pro recommended, relay provider application URL: https://aihubmix.com/?aff=8Ds9) API key")
    MEDIA_ENGINE_BASE_URL: Optional[str] = Field("https://aihubmix.com/v1", description="Media Agent LLM base URL, adjustable based on relay service")
    MEDIA_ENGINE_MODEL_NAME: str = Field("gemini-2.5-pro", description="Media Agent LLM model name, e.g., gemini-2.5-pro")
    
    # Query Agent (DeepSeek recommended, application URL: https://www.deepseek.com/)
    QUERY_ENGINE_API_KEY: Optional[str] = Field(None, description="Query Agent (deepseek recommended, official application URL: https://platform.deepseek.com/) API key")
    QUERY_ENGINE_BASE_URL: Optional[str] = Field("https://api.deepseek.com", description="Query Agent LLM base URL")
    QUERY_ENGINE_MODEL_NAME: str = Field("deepseek-chat", description="Query Agent LLM model name, e.g., deepseek-reasoner")
    
    # Report Agent (Gemini recommended, relay provider recommended: https://aihubmix.com/?aff=8Ds9)
    REPORT_ENGINE_API_KEY: Optional[str] = Field(None, description="Report Agent (gemini-2.5-pro recommended, relay provider application URL: https://aihubmix.com/?aff=8Ds9) API key")
    REPORT_ENGINE_BASE_URL: Optional[str] = Field("https://aihubmix.com/v1", description="Report Agent LLM base URL, adjustable based on relay service")
    REPORT_ENGINE_MODEL_NAME: str = Field("gemini-2.5-pro", description="Report Agent LLM model name, e.g., gemini-2.5-pro")

    # MindSpider Agent (Deepseek recommended, official application URL: https://platform.deepseek.com/)
    MINDSPIDER_API_KEY: Optional[str] = Field(None, description="MindSpider Agent (deepseek recommended, official application URL: https://platform.deepseek.com/) API key")
    MINDSPIDER_BASE_URL: Optional[str] = Field(None, description="MindSpider Agent base URL, configurable based on selected service")
    MINDSPIDER_MODEL_NAME: Optional[str] = Field(None, description="MindSpider Agent model name, e.g., deepseek-reasoner")
    
    # Forum Host (Latest Qwen3 model, using SiliconFlow platform, application URL: https://cloud.siliconflow.cn/)
    FORUM_HOST_API_KEY: Optional[str] = Field(None, description="Forum Host (qwen-plus recommended, official application URL: https://www.aliyun.com/product/bailian) API key")
    FORUM_HOST_BASE_URL: Optional[str] = Field(None, description="Forum Host LLM base URL, configurable based on selected service")
    FORUM_HOST_MODEL_NAME: Optional[str] = Field(None, description="Forum Host LLM model name, e.g., qwen-plus")
    
    # SQL keyword Optimizer (Small parameter Qwen3 model, using SiliconFlow platform, application URL: https://cloud.siliconflow.cn/)
    KEYWORD_OPTIMIZER_API_KEY: Optional[str] = Field(None, description="SQL Keyword Optimizer (qwen-plus recommended, official application URL: https://www.aliyun.com/product/bailian) API key")
    KEYWORD_OPTIMIZER_BASE_URL: Optional[str] = Field(None, description="Keyword Optimizer base URL, configurable based on selected service")
    KEYWORD_OPTIMIZER_MODEL_NAME: Optional[str] = Field(None, description="Keyword Optimizer LLM model name, e.g., qwen-plus")
    
    # ================== Network Tools Configuration ====================
    # Tavily API (application URL: https://www.tavily.com/)
    TAVILY_API_KEY: Optional[str] = Field(None, description="Tavily API (application URL: https://www.tavily.com/) API key for Tavily web search")

    # Bocha API (application URL: https://open.bochaai.com/)
    BOCHA_BASE_URL: Optional[str] = Field("https://api.bochaai.com/v1/ai-search", description="Bocha AI search base URL or Bocha web search base URL")
    BOCHA_WEB_SEARCH_API_KEY: Optional[str] = Field(None, description="Bocha API (application URL: https://open.bochaai.com/) API key for Bocha search")
    
    # ================== Insight Engine Search Configuration ====================
    DEFAULT_SEARCH_HOT_CONTENT_LIMIT: int = Field(100, description="Default maximum number of trending content items")
    DEFAULT_SEARCH_TOPIC_GLOBALLY_LIMIT_PER_TABLE: int = Field(50, description="Maximum number of global topics per table")
    DEFAULT_SEARCH_TOPIC_BY_DATE_LIMIT_PER_TABLE: int = Field(100, description="Maximum number of topics by date per table")
    DEFAULT_GET_COMMENTS_FOR_TOPIC_LIMIT: int = Field(500, description="Maximum number of comments per topic")
    DEFAULT_SEARCH_TOPIC_ON_PLATFORM_LIMIT: int = Field(200, description="Maximum number of platform search topics")
    MAX_SEARCH_RESULTS_FOR_LLM: int = Field(0, description="Maximum number of search results for LLM")
    MAX_HIGH_CONFIDENCE_SENTIMENT_RESULTS: int = Field(0, description="Maximum number of high-confidence sentiment analysis results")
    MAX_REFLECTIONS: int = Field(3, description="Maximum number of reflections")
    MAX_PARAGRAPHS: int = Field(6, description="Maximum number of paragraphs")
    SEARCH_TIMEOUT: int = Field(240, description="Single search request timeout in seconds")
    MAX_CONTENT_LENGTH: int = Field(500000, description="Maximum search content length")
    
    model_config = ConfigDict(
        env_file=ENV_FILE,
        env_prefix="",
        case_sensitive=False,
        extra="allow"
    )


# Create global configuration instance
settings = Settings()


def reload_settings() -> Settings:
    """
    Reload configuration

    Reload configuration from .env file and environment variables, updating the global settings instance.
    Used for dynamically updating configuration at runtime.

    Returns:
        Settings: Newly created configuration instance
    """
    
    global settings
    settings = Settings()
    return settings
