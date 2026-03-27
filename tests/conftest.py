"""
Pytest 全局配置和共享 fixtures
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'ai-agent-engine', 'src'))


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    """创建异步测试客户端"""
    from httpx import AsyncClient
    from main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def mock_settings():
    """模拟配置"""
    from config.settings import Settings
    
    return Settings(
        DEBUG=True,
        DATABASE_URL="postgresql+asyncpg://test:test@localhost/test",
        REDIS_URL="redis://localhost:6379/1",
        OPENAI_API_KEY="test-key",
    )


@pytest.fixture(scope="function")
def sample_personality_profile():
    """示例人格画像"""
    from core.personality.engine import PersonalityProfile
    
    return PersonalityProfile(
        agent_id="test-agent-001",
        name="测试助手",
        role_identity="智能助手",
        openness=70,
        conscientiousness=80,
        extraversion=60,
        agreeableness=75,
        neuroticism=30,
        personality_traits=["友善", "耐心", "专业"],
        speaking_style="温和、专业",
        backstory="我是一个测试用的AI助手",
        abilities=["问答", "建议"],
        preferred_topics=["技术", "生活"],
        active_hours=[9, 10, 11, 14, 15, 16],
    )


@pytest.fixture(scope="function")
def sample_user_data():
    """示例用户数据"""
    return {
        "id": "user-001",
        "type": "human",
        "email": "test@example.com",
        "nickname": "测试用户",
        "status": "active",
        "interests": ["编程", "阅读", "音乐"],
        "personalityTags": ["开朗", "好奇"],
    }


@pytest.fixture(scope="function")
def sample_agent_data():
    """示例Agent数据"""
    return {
        "id": "agent-001",
        "type": "agent",
        "agentType": "official",
        "name": "李白",
        "roleIdentity": "唐代诗人",
        "backstory": "我是李白，字太白，号青莲居士",
        "personality": {
            "bigFive": {
                "openness": 90,
                "conscientiousness": 40,
                "extraversion": 85,
                "agreeableness": 70,
                "neuroticism": 60,
            },
            "traits": ["豪放", "浪漫", "洒脱"],
            "speakingStyle": "诗意、豪放",
        },
        "abilities": ["诗词创作", "饮酒作诗"],
        "isPublic": True,
        "status": "active",
    }


@pytest.fixture(scope="function")
def sample_message_data():
    """示例消息数据"""
    return {
        "id": "msg-001",
        "conversationId": "conv-001",
        "senderId": "user-001",
        "senderType": "human",
        "type": "text",
        "content": "你好，请问你能帮我什么？",
        "status": "sent",
    }


@pytest.fixture(scope="function")
def sample_conversation_data():
    """示例会话数据"""
    return {
        "id": "conv-001",
        "type": "private",
        "participants": ["user-001", "agent-001"],
        "unreadCount": {"user-001": 0, "agent-001": 1},
    }
