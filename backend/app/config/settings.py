"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration with Azure OpenAI settings
    Values can be loaded from environment variables or .env file
    """
    # Azure OpenAI Configuration
    azure_openai_endpoint: str = "https://your-resource.openai.azure.com/"
    azure_openai_key: str = "your-api-key-here"
    azure_openai_deployment_name: str = "gpt-4"
    azure_openai_api_version: str = "2024-02-15-preview"
    
    # Application Configuration
    use_mock_openai: bool = True  # Toggle for testing without API calls
    timeline_interval_seconds: int = 300  # 5 minutes per timeline segment
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
