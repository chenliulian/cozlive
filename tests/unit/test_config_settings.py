"""
配置管理单元测试
测试 AI Agent Engine 的配置加载和验证
"""

import pytest
import os
from unittest.mock import patch
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'ai-agent-engine', 'src'))


class TestSettings:
    """测试配置类"""
    
    def test_default_settings(self):
        """测试默认配置值"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 基础配置
        assert settings.APP_NAME == "Cozlive AI Agent Engine"
        assert settings.DEBUG == False
        assert settings.HOST == "0.0.0.0"
        assert settings.PORT == 8000
        assert settings.WORKERS == 4
    
    def test_cors_origins_default(self):
        """测试默认 CORS 配置"""
        from config.settings import Settings
        
        settings = Settings()
        assert settings.CORS_ORIGINS == ["*"]
    
    def test_database_urls(self):
        """测试数据库 URL 配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 验证数据库 URL 不为空
        assert settings.DATABASE_URL is not None
        assert settings.MONGODB_URL is not None
        assert settings.REDIS_URL is not None
    
    def test_vector_store_config(self):
        """测试向量数据库配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert settings.VECTOR_STORE_TYPE in ["chroma", "pinecone", "qdrant"]
        assert settings.CHROMA_PERSIST_DIRECTORY is not None
    
    def test_llm_config(self):
        """测试 LLM 配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert settings.DEFAULT_LLM_MODEL is not None
        assert settings.DEFAULT_EMBEDDING_MODEL is not None
    
    def test_agent_config(self):
        """测试 Agent 配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert settings.MAX_AGENTS_PER_USER > 0
        assert settings.AGENT_MEMORY_TTL > 0
        assert settings.MAX_CONTEXT_LENGTH > 0
    
    def test_personality_dimensions(self):
        """测试人格维度配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        expected_dimensions = [
            "openness",
            "conscientiousness",
            "extraversion",
            "agreeableness",
            "neuroticism",
        ]
        
        assert settings.PERSONALITY_DIMENSIONS == expected_dimensions
    
    def test_emotion_config(self):
        """测试情感计算配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert isinstance(settings.EMOTION_DETECTION_ENABLED, bool)
        assert 0 <= settings.EMOTION_INTENSITY_THRESHOLD <= 1
    
    def test_memory_config(self):
        """测试记忆配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert 0 <= settings.MEMORY_SIMILARITY_THRESHOLD <= 1
        assert settings.MEMORY_MAX_RESULTS > 0
        assert settings.MEMORY_SUMMARY_INTERVAL > 0
    
    def test_evolution_config(self):
        """测试进化配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert isinstance(settings.EVOLUTION_ENABLED, bool)
        assert settings.EVOLUTION_INTERVAL > 0
        assert settings.MIN_INTERACTIONS_FOR_EVOLUTION > 0
    
    def test_autonomous_behavior_config(self):
        """测试自主行为配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert isinstance(settings.AUTONOMOUS_BEHAVIOR_ENABLED, bool)
        assert settings.AUTONOMOUS_BEHAVIOR_INTERVAL > 0
    
    def test_kafka_config(self):
        """测试 Kafka 配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert settings.KAFKA_BOOTSTRAP_SERVERS is not None
        assert settings.KAFKA_TOPIC_AGENT_EVENTS is not None
        assert settings.KAFKA_TOPIC_CHAT_MESSAGES is not None
    
    def test_monitoring_config(self):
        """测试监控配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert settings.PROMETHEUS_PORT > 0
    
    def test_logging_config(self):
        """测试日志配置"""
        from config.settings import Settings
        
        settings = Settings()
        
        assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert settings.LOG_FORMAT in ["json", "text"]


class TestSettingsEnvironment:
    """测试环境变量配置"""
    
    @patch.dict(os.environ, {"DEBUG": "true"})
    def test_debug_from_env(self):
        """测试从环境变量读取 DEBUG"""
        from config.settings import Settings
        
        settings = Settings()
        assert settings.DEBUG == True
    
    @patch.dict(os.environ, {"PORT": "9000"})
    def test_port_from_env(self):
        """测试从环境变量读取 PORT"""
        from config.settings import Settings
        
        settings = Settings()
        assert settings.PORT == 9000
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    def test_openai_key_from_env(self):
        """测试从环境变量读取 OpenAI API Key"""
        from config.settings import Settings
        
        settings = Settings()
        assert settings.OPENAI_API_KEY == "test-api-key"
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "[\"http://localhost:3000\", \"https://example.com\"]"})
    def test_cors_origins_from_env(self):
        """测试从环境变量读取 CORS_ORIGINS"""
        from config.settings import Settings
        
        settings = Settings()
        assert "http://localhost:3000" in settings.CORS_ORIGINS


class TestSettingsValidation:
    """测试配置验证"""
    
    def test_port_range_validation(self):
        """测试端口范围验证"""
        from config.settings import Settings
        
        # 有效端口
        settings = Settings(PORT=8080)
        assert settings.PORT == 8080
        
        # 边界端口
        settings = Settings(PORT=1)
        assert settings.PORT == 1
        
        settings = Settings(PORT=65535)
        assert settings.PORT == 65535
    
    def test_workers_positive(self):
        """测试工作进程数为正数"""
        from config.settings import Settings
        
        settings = Settings(WORKERS=4)
        assert settings.WORKERS == 4
        assert settings.WORKERS > 0
    
    def test_memory_threshold_range(self):
        """测试记忆相似度阈值范围"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 阈值应在 0-1 之间
        assert 0 <= settings.MEMORY_SIMILARITY_THRESHOLD <= 1
    
    def test_emotion_threshold_range(self):
        """测试情感强度阈值范围"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 阈值应在 0-1 之间
        assert 0 <= settings.EMOTION_INTENSITY_THRESHOLD <= 1


class TestSettingsSingleton:
    """测试配置单例"""
    
    def test_settings_singleton(self):
        """测试配置单例模式"""
        from config.settings import settings, Settings
        
        # 验证全局设置实例
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_settings_immutability(self):
        """测试配置不可变性（尝试修改）"""
        from config.settings import Settings
        
        settings1 = Settings(DEBUG=True)
        settings2 = Settings(DEBUG=False)
        
        # 不同实例应独立
        assert settings1.DEBUG == True
        assert settings2.DEBUG == False
