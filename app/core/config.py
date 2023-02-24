from pydantic import BaseSettings

class Settings(BaseSettings):
    SERVER_HOST: str 
    SERVER_PORT: int 
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    CONTAINER_DB_PORT: str
    REDIS_URL: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()