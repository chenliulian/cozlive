"""
配置管理
"""

from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    APP_NAME: str = "Cozlive AI Agent Engine"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/cozlive"
    MONGODB_URL: str = "mongodb://localhost:27017/cozlive"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 向量数据库
    VECTOR_STORE_TYPE: str = "chroma"  # chroma, pinecone, qdrant
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    QDRANT_URL: Optional[str] = None
    
    # LLM 配置
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "gpt-4"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # Agent 配置
    MAX_AGENTS_PER_USER: int = 100
    AGENT_MEMORY_TTL: int = 86400  # 24小时
    MAX_CONTEXT_LENGTH: int = 8192
    
    # 人格模型配置
    PERSONALITY_DIMENSIONS: List[str] = [
        "openness",           # 开放性
        "conscientiousness",  # 责任心
        "extraversion",       # 外向性
        "agreeableness",      # 宜人性
        "neuroticism",        # 神经质
    ]
    
    # 情感计算配置
    EMOTION_DETECTION_ENABLED: bool = True
    EMOTION_INTENSITY_THRESHOLD: float = 0.3
    
    # 记忆配置
    MEMORY_SIMILARITY_THRESHOLD: float = 0.75
    MEMORY_MAX_RESULTS: int = 10
    MEMORY_SUMMARY_INTERVAL: int = 86400  # 24小时
    
    # 进化配置
    EVOLUTION_ENABLED: bool = True
    EVOLUTION_INTERVAL: int = 604800  # 7天
    MIN_INTERACTIONS_FOR_EVOLUTION: int = 50
    
    # 自主行为配置
    AUTONOMOUS_BEHAVIOR_ENABLED: bool = True
    AUTONOMOUS_BEHAVIOR_INTERVAL: int = 300  # 5分钟
    
    # 消息队列
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_AGENT_EVENTS: str = "agent-events"
    KAFKA_TOPIC_CHAT_MESSAGES: str = "chat-messages"
    
    # 监控
    PROMETHEUS_PORT: int = 9090
    SENTRY_DSN: Optional[str] = None
    
    # 日志
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局配置实例
settings = Settings()
