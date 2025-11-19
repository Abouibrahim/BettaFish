"""
Configuration management module for the Media Engine (pydantic_settings style).
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


# Calculate .env priority: prioritize current working directory, then project root
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
CWD_ENV: Path = Path.cwd() / ".env"
ENV_FILE: str = str(CWD_ENV if CWD_ENV.exists() else (PROJECT_ROOT / ".env"))

class Settings(BaseSettings):
    """
    Global configuration; supports automatic loading of .env and environment variables.
    Variable names are consistent with original config.py uppercase for smooth transition.
    """
    # ====================== Database Configuration ======================
    DB_HOST: str = Field("your_db_host", description="Database host, e.g., localhost or 127.0.0.1. We also provide cloud database resources for convenient configuration with 100k+ daily data. Free application available, contact us: 670939375@qq.com NOTE: Due to data compliance review and service upgrades, cloud database will suspend new application acceptance from October 1, 2025")
    DB_PORT: int = Field(3306, description="Database port number, default is 3306")
    DB_USER: str = Field("your_db_user", description="Database username")
    DB_PASSWORD: str = Field("your_db_password", description="Database password")
    DB_NAME: str = Field("your_db_name", description="Database name")
    DB_CHARSET: str = Field("utf8mb4", description="Database charset, recommended utf8mb4, compatible with emoji")
    DB_DIALECT: str = Field("mysql", description="Database type, e.g., 'mysql' or 'postgresql'. Used to support multiple database backends (such as SQLAlchemy, configure together with connection information)")

    # ======================= LLM Related =======================
    INSIGHT_ENGINE_API_KEY: str = Field(None, description="Insight Agent (recommended Kimi, https://platform.moonshot.cn/) API key for main LLM. You can change the API used by each component's LLM. As long as it's compatible with OpenAI request format, you can use it normally by defining KEY, BASE_URL, and MODEL_NAME. Important reminder: We strongly recommend you first apply for API using the recommended configuration, get it running first, then make your changes!")
    INSIGHT_ENGINE_BASE_URL: Optional[str] = Field("https://api.moonshot.cn/v1", description="Insight Agent LLM interface BaseUrl, can customize vendor API")
    INSIGHT_ENGINE_MODEL_NAME: str = Field("kimi-k2-0711-preview", description="Insight Agent LLM model name, such as kimi-k2-0711-preview")

    MEDIA_ENGINE_API_KEY: str = Field(None, description="Media Agent (recommended Gemini, here I used a relay vendor, you can also replace with your own, application address: https://www.chataiapi.com/) API key")
    MEDIA_ENGINE_BASE_URL: Optional[str] = Field("https://www.chataiapi.com/v1", description="Media Agent LLM interface BaseUrl")
    MEDIA_ENGINE_MODEL_NAME: str = Field("gemini-2.5-pro", description="Media Agent LLM model name, such as gemini-2.5-pro")
    
    BOCHA_WEB_SEARCH_API_KEY: Optional[str] = Field(None, description="Bocha Web Search API Key")
    BOCHA_API_KEY: Optional[str] = Field(None, description="Bocha compatible key (alias)")

    SEARCH_TIMEOUT: int = Field(240, description="Search timeout (seconds)")
    SEARCH_CONTENT_MAX_LENGTH: int = Field(20000, description="Maximum content length for prompts")
    MAX_REFLECTIONS: int = Field(2, description="Maximum reflection rounds")
    MAX_PARAGRAPHS: int = Field(5, description="Maximum paragraphs")

    MINDSPIDER_API_KEY: Optional[str] = Field(None, description="MindSpider API key")
    MINDSPIDER_BASE_URL: Optional[str] = Field("https://api.deepseek.com", description="MindSpider LLM interface BaseUrl")
    MINDSPIDER_MODEL_NAME: str = Field("deepseek-reasoner", description="MindSpider LLM model name, such as deepseek-reasoner")

    OUTPUT_DIR: str = Field("reports", description="Output directory")
    SAVE_INTERMEDIATE_STATES: bool = Field(True, description="Whether to save intermediate states")



    QUERY_ENGINE_API_KEY: str = Field(None, description="Query Agent (recommended DeepSeek, https://www.deepseek.com/) API key")
    QUERY_ENGINE_BASE_URL: Optional[str] = Field("https://api.deepseek.com", description="Query Agent LLM interface BaseUrl")
    QUERY_ENGINE_MODEL_NAME: str = Field("deepseek-reasoner", description="Query Agent LLM model, such as deepseek-reasoner")

    REPORT_ENGINE_API_KEY: str = Field(None, description="Report Agent (recommended Gemini, here I used a relay vendor, you can also replace with your own, application address: https://www.chataiapi.com/) API key")
    REPORT_ENGINE_BASE_URL: Optional[str] = Field("https://www.chataiapi.com/v1", description="Report Agent LLM interface BaseUrl")
    REPORT_ENGINE_MODEL_NAME: str = Field("gemini-2.5-pro", description="Report Agent LLM model, such as gemini-2.5-pro")

    FORUM_HOST_API_KEY: str = Field(None, description="Forum Host (latest Qwen3 model, here I used the SiliconFlow platform, application address: https://cloud.siliconflow.cn/) API key")
    FORUM_HOST_BASE_URL: Optional[str] = Field("https://api.siliconflow.cn/v1", description="Forum Host LLM BaseUrl")
    FORUM_HOST_MODEL_NAME: str = Field("Qwen/Qwen3-235B-A22B-Instruct-2507", description="Forum Host LLM model name, such as Qwen/Qwen3-235B-A22B-Instruct-2507")

    KEYWORD_OPTIMIZER_API_KEY: str = Field(None, description="SQL keyword Optimizer (small parameter Qwen3 model, here I used the SiliconFlow platform, application address: https://cloud.siliconflow.cn/) API key")
    KEYWORD_OPTIMIZER_BASE_URL: Optional[str] = Field("https://api.siliconflow.cn/v1", description="Keyword Optimizer BaseUrl")
    KEYWORD_OPTIMIZER_MODEL_NAME: str = Field("Qwen/Qwen3-30B-A3B-Instruct-2507", description="Keyword Optimizer LLM model name, such as Qwen/Qwen3-30B-A3B-Instruct-2507")

    # ================== Network Tools Configuration ====================
    TAVILY_API_KEY: str = Field(None, description="Tavily API (application address: https://www.tavily.com/) API key for Tavily web search")
    BOCHA_BASE_URL: Optional[str] = Field("https://api.bochaai.com/v1/ai-search", description="Bocha AI search BaseUrl or Bocha web search BaseUrl")
    BOCHA_WEB_SEARCH_API_KEY: str = Field(None, description="Bocha API (application address: https://open.bochaai.com/) API key for Bocha search")

    class Config:
        env_file = ENV_FILE
        env_prefix = ""
        case_sensitive = False
        extra = "allow"


settings = Settings()
