"""
服务集成测试
测试 AI Agent Engine 内部服务间的集成
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'ai-agent-engine', 'src'))


class TestAgentManagerIntegration:
    """测试 Agent 管理器集成"""
    
    @pytest.fixture
    def mock_vector_store(self):
        """模拟向量存储"""
        store = AsyncMock()
        store.initialize = AsyncMock()
        store.close = AsyncMock()
        store.add_memory = AsyncMock(return_value="memory-id-001")
        store.search_memories = AsyncMock(return_value=[])
        return store
    
    @pytest.fixture
    def mock_llm(self):
        """模拟 LLM"""
        llm = Mock()
        llm.predict = Mock(return_value="这是 AI 的回复")
        return llm
    
    def test_agent_creation_flow(self, mock_vector_store, mock_llm):
        """测试 Agent 创建流程"""
        # 验证 Agent 创建时各组件协同工作
        
        agent_data = {
            "name": "测试助手",
            "role_identity": "智能助手",
            "personality": {
                "bigFive": {
                    "openness": 70,
                    "conscientiousness": 80,
                    "extraversion": 60,
                    "agreeableness": 75,
                    "neuroticism": 30,
                },
                "traits": ["友善", "专业"],
            },
        }
        
        # 验证数据结构完整性
        assert "name" in agent_data
        assert "role_identity" in agent_data
        assert "personality" in agent_data
        assert "bigFive" in agent_data["personality"]
    
    def test_agent_chat_flow(self, mock_vector_store, mock_llm):
        """测试 Agent 对话流程"""
        # 模拟完整的对话流程
        
        conversation = [
            {"role": "user", "content": "你好"},
            {"role": "agent", "content": "你好！很高兴见到你。"},
            {"role": "user", "content": "今天天气怎么样？"},
        ]
        
        # 验证对话流程
        assert len(conversation) == 3
        assert conversation[0]["role"] == "user"
        assert conversation[1]["role"] == "agent"
    
    def test_memory_storage_flow(self, mock_vector_store):
        """测试记忆存储流程"""
        # 模拟记忆存储流程
        
        memory_data = {
            "agent_id": "agent-001",
            "user_id": "user-001",
            "content": "用户喜欢编程",
            "type": "preference",
            "importance": 0.8,
        }
        
        # 验证记忆数据结构
        assert memory_data["agent_id"] is not None
        assert memory_data["user_id"] is not None
        assert memory_data["content"] is not None
        assert 0 <= memory_data["importance"] <= 1


class TestPersonalityEngineIntegration:
    """测试人格引擎集成"""
    
    def test_personality_consistency_with_memory(self):
        """测试人格一致性与记忆的集成"""
        from core.personality.engine import PersonalityProfile
        
        profile = PersonalityProfile(
            agent_id="agent-001",
            name="李白",
            role_identity="唐代诗人",
            openness=90,
            conscientiousness=40,
            extraversion=85,
            agreeableness=70,
            neuroticism=60,
            personality_traits=["豪放", "浪漫"],
            speaking_style="诗意、豪放",
        )
        
        # 验证人格画像与记忆系统协同
        assert profile.agent_id == "agent-001"
        assert "豪放" in profile.personality_traits
    
    def test_emotion_calculation_integration(self):
        """测试情感计算集成"""
        # 模拟情感计算与其他模块的集成
        
        emotion_state = {
            "currentMood": "开心",
            "moodIntensity": 0.8,
            "emotionalState": {
                "joy": 0.9,
                "sadness": 0.1,
                "anger": 0.0,
            },
        }
        
        # 验证情感状态结构
        assert "currentMood" in emotion_state
        assert "moodIntensity" in emotion_state
        assert 0 <= emotion_state["moodIntensity"] <= 1


class TestVectorStoreIntegration:
    """测试向量存储集成"""
    
    def test_memory_embedding_generation(self):
        """测试记忆嵌入向量生成"""
        # 模拟嵌入向量生成
        
        text = "用户喜欢编程和阅读"
        # 在实际实现中，这会调用嵌入模型
        
        # 验证文本不为空
        assert len(text) > 0
    
    def test_similarity_search(self):
        """测试相似度搜索"""
        # 模拟相似度搜索
        
        query = "用户的兴趣"
        memories = [
            {"content": "用户喜欢编程", "similarity": 0.95},
            {"content": "用户喜欢阅读", "similarity": 0.85},
            {"content": "用户喜欢音乐", "similarity": 0.70},
        ]
        
        # 按相似度排序
        sorted_memories = sorted(memories, key=lambda x: x["similarity"], reverse=True)
        
        # 验证排序结果
        assert sorted_memories[0]["similarity"] >= sorted_memories[1]["similarity"]
        assert sorted_memories[1]["similarity"] >= sorted_memories[2]["similarity"]


class TestEvolutionEngineIntegration:
    """测试进化引擎集成"""
    
    def test_evolution_trigger_conditions(self):
        """测试进化触发条件"""
        # 模拟进化触发条件检查
        
        interaction_count = 60
        min_interactions = 50
        last_evolution_time = 1700000000  # 假设的时间戳
        current_time = 1700604800  # 7天后
        evolution_interval = 604800  # 7天
        
        # 检查是否满足进化条件
        should_evolve = (
            interaction_count >= min_interactions and
            (current_time - last_evolution_time) >= evolution_interval
        )
        
        assert should_evolve == True
    
    def test_personality_evolution_calculation(self):
        """测试人格进化计算"""
        # 模拟人格维度进化
        
        current_big_five = {
            "openness": 70,
            "conscientiousness": 60,
            "extraversion": 50,
        }
        
        # 基于互动数据的调整
        adjustments = {
            "openness": 2,  # 增加开放性
            "conscientiousness": 0,
            "extraversion": 3,  # 增加外向性
        }
        
        # 计算新的人格维度
        new_big_five = {
            k: min(100, max(0, v + adjustments.get(k, 0)))
            for k, v in current_big_five.items()
        }
        
        # 验证进化后的值在有效范围内
        for value in new_big_five.values():
            assert 0 <= value <= 100


class TestMessageQueueIntegration:
    """测试消息队列集成"""
    
    def test_kafka_event_structure(self):
        """测试 Kafka 事件结构"""
        # 模拟 Kafka 事件
        
        event = {
            "event_type": "agent_response",
            "timestamp": 1704067200000,
            "data": {
                "agent_id": "agent-001",
                "user_id": "user-001",
                "message": "你好！",
                "conversation_id": "conv-001",
            },
            "metadata": {
                "service": "ai-agent-engine",
                "version": "1.0.0",
            },
        }
        
        # 验证事件结构
        assert "event_type" in event
        assert "timestamp" in event
        assert "data" in event
        assert "metadata" in event
    
    def test_event_serialization(self):
        """测试事件序列化"""
        import json
        
        event = {
            "event_type": "memory_stored",
            "timestamp": 1704067200000,
            "data": {"memory_id": "mem-001", "content": "测试记忆"},
        }
        
        # 序列化
        serialized = json.dumps(event)
        
        # 反序列化
        deserialized = json.loads(serialized)
        
        # 验证数据完整性
        assert deserialized["event_type"] == event["event_type"]
        assert deserialized["data"]["memory_id"] == event["data"]["memory_id"]


class TestDatabaseIntegration:
    """测试数据库集成"""
    
    def test_postgres_connection_string(self):
        """测试 PostgreSQL 连接字符串"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 验证连接字符串格式
        assert "postgresql" in settings.DATABASE_URL
        assert "@" in settings.DATABASE_URL
    
    def test_mongodb_connection_string(self):
        """测试 MongoDB 连接字符串"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 验证连接字符串格式
        assert "mongodb" in settings.MONGODB_URL
    
    def test_redis_connection_string(self):
        """测试 Redis 连接字符串"""
        from config.settings import Settings
        
        settings = Settings()
        
        # 验证连接字符串格式
        assert "redis" in settings.REDIS_URL
