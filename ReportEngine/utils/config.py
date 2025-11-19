"""
Configuration management module for the Report Engine.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

from loguru import logger

class Settings(BaseSettings):
    """Report Engine configuration, environment variables and fields use consistent uppercase REPORT_ENGINE_ prefix."""
    REPORT_ENGINE_API_KEY: Optional[str] = Field(None, description="Report Engine LLM API key")
    REPORT_ENGINE_BASE_URL: Optional[str] = Field(None, description="Report Engine LLM base URL")
    REPORT_ENGINE_MODEL_NAME: Optional[str] = Field(None, description="Report Engine LLM model name")
    REPORT_ENGINE_PROVIDER: Optional[str] = Field(None, description="Model service provider, kept for compatibility only")
    MAX_CONTENT_LENGTH: int = Field(200000, description="Maximum content length")
    OUTPUT_DIR: str = Field("final_reports", description="Main output directory")
    TEMPLATE_DIR: str = Field("ReportEngine/report_template", description="Multi-template directory")
    API_TIMEOUT: float = Field(900.0, description="Single API timeout (seconds)")
    MAX_RETRY_DELAY: float = Field(180.0, description="Maximum retry interval (seconds)")
    MAX_RETRIES: int = Field(8, description="Maximum retry attempts")
    LOG_FILE: str = Field("logs/report.log", description="Log output file")
    ENABLE_PDF_EXPORT: bool = Field(True, description="Whether to allow PDF export")
    CHART_STYLE: str = Field("modern", description="Chart style: modern/classic/")

    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False
        extra = "allow"

settings = Settings()


def print_config(config: Settings):
    message = ""
    message += "\n=== Report Engine Configuration ===\n"
    message += f"LLM Model: {config.REPORT_ENGINE_MODEL_NAME}\n"
    message += f"LLM Base URL: {config.REPORT_ENGINE_BASE_URL or '(default)'}\n"
    message += f"Max Content Length: {config.MAX_CONTENT_LENGTH}\n"
    message += f"Output Directory: {config.OUTPUT_DIR}\n"
    message += f"Template Directory: {config.TEMPLATE_DIR}\n"
    message += f"API Timeout: {config.API_TIMEOUT} seconds\n"
    message += f"Max Retry Delay: {config.MAX_RETRY_DELAY} seconds\n"
    message += f"Max Retries: {config.MAX_RETRIES}\n"
    message += f"Log File: {config.LOG_FILE}\n"
    message += f"PDF Export: {config.ENABLE_PDF_EXPORT}\n"
    message += f"Chart Style: {config.CHART_STYLE}\n"
    message += f"LLM API Key: {'Configured' if config.REPORT_ENGINE_API_KEY else 'Not configured'}\n"
    message += "===================================\n"
    logger.info(message)
