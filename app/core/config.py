import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "Desenvolvimento de um Agente AI Personalizado com AWS AgentCore"
    VERSION: str = "1.0.0"
    AUTHOR: str = "Felipe Madison (@FelipeMadson)"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "enterprise-ai-python-secret-32b-key")
    EMBEDDING_DIM: int = 64
    MAX_AGENT_ITERATIONS: int = 5

settings = Settings()
