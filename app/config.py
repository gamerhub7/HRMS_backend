from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/hrms_lite"
    
    # CORS - will include production frontend URL
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Application
    app_name: str = "HRMS Lite API"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
