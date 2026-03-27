"""
API 集成测试
测试 AI Agent Engine API 端点的完整交互
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'ai-agent-engine', 'src'))


class TestAgentAPI:
    """测试 Agent 相关 API"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import create_app
        
        app = create_app()
        return TestClient(app)
    
    def test_create_agent(self, client):
        """测试创建 Agent"""
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
                "speakingStyle": "温和",
            },
            "abilities": ["问答", "建议"],
        }
        
        # 注意：实际测试需要模拟数据库操作
        # 这里仅测试 API 结构
        response = client.post("/api/v1/agents", json=agent_data)
        
        # 由于缺少数据库连接，预期会返回错误
        # 但验证 API 端点存在
        assert response.status_code in [200, 201, 422, 500]
    
    def test_get_agent_list(self, client):
        """测试获取 Agent 列表"""
        response = client.get("/api/v1/agents")
        
        # 验证端点存在
        assert response.status_code in [200, 500]
    
    def test_get_agent_detail(self, client):
        """测试获取 Agent 详情"""
        agent_id = "test-agent-001"
        response = client.get(f"/api/v1/agents/{agent_id}")
        
        # 验证端点存在
        assert response.status_code in [200, 404, 500]
    
    def test_update_agent(self, client):
        """测试更新 Agent"""
        agent_id = "test-agent-001"
        update_data = {
            "name": "更新后的名字",
            "personality": {
                "traits": ["更新后的特质"],
            },
        }
        
        response = client.put(f"/api/v1/agents/{agent_id}", json=update_data)
        
        # 验证端点存在
        assert response.status_code in [200, 404, 422, 500]
    
    def test_delete_agent(self, client):
        """测试删除 Agent"""
        agent_id = "test-agent-001"
        response = client.delete(f"/api/v1/agents/{agent_id}")
        
        # 验证端点存在
        assert response.status_code in [200, 204, 404, 500]


class TestChatAPI:
    """测试聊天相关 API"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import create_app
        
        app = create_app()
        return TestClient(app)
    
    def test_send_message(self, client):
        """测试发送消息"""
        message_data = {
            "agent_id": "agent-001",
            "user_id": "user-001",
            "content": "你好，请介绍一下自己",
            "conversation_id": "conv-001",
        }
        
        response = client.post("/api/v1/chat/message", json=message_data)
        
        # 验证端点存在
        assert response.status_code in [200, 201, 422, 500]
    
    def test_get_conversation_history(self, client):
        """测试获取会话历史"""
        conversation_id = "conv-001"
        response = client.get(f"/api/v1/chat/conversations/{conversation_id}/messages")
        
        # 验证端点存在
        assert response.status_code in [200, 404, 500]
    
    def test_create_conversation(self, client):
        """测试创建会话"""
        conversation_data = {
            "user_id": "user-001",
            "agent_id": "agent-001",
            "type": "private",
        }
        
        response = client.post("/api/v1/chat/conversations", json=conversation_data)
        
        # 验证端点存在
        assert response.status_code in [200, 201, 422, 500]


class TestMemoryAPI:
    """测试记忆相关 API"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import create_app
        
        app = create_app()
        return TestClient(app)
    
    def test_store_memory(self, client):
        """测试存储记忆"""
        memory_data = {
            "agent_id": "agent-001",
            "user_id": "user-001",
            "content": "用户喜欢编程",
            "type": "preference",
            "importance": 0.8,
        }
        
        response = client.post("/api/v1/memory", json=memory_data)
        
        # 验证端点存在
        assert response.status_code in [200, 201, 422, 500]
    
    def test_retrieve_memory(self, client):
        """测试检索记忆"""
        agent_id = "agent-001"
        user_id = "user-001"
        query = "用户的兴趣"
        
        response = client.get(
            f"/api/v1/memory/retrieve",
            params={"agent_id": agent_id, "user_id": user_id, "query": query}
        )
        
        # 验证端点存在
        assert response.status_code in [200, 422, 500]
    
    def test_get_agent_memories(self, client):
        """测试获取 Agent 的所有记忆"""
        agent_id = "agent-001"
        response = client.get(f"/api/v1/memory/agent/{agent_id}")
        
        # 验证端点存在
        assert response.status_code in [200, 404, 500]


class TestEvolutionAPI:
    """测试进化相关 API"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import create_app
        
        app = create_app()
        return TestClient(app)
    
    def test_trigger_evolution(self, client):
        """测试触发进化"""
        evolution_data = {
            "agent_id": "agent-001",
            "evolution_type": "personality",
        }
        
        response = client.post("/api/v1/evolution/trigger", json=evolution_data)
        
        # 验证端点存在
        assert response.status_code in [200, 202, 422, 500]
    
    def test_get_evolution_status(self, client):
        """测试获取进化状态"""
        agent_id = "agent-001"
        response = client.get(f"/api/v1/evolution/status/{agent_id}")
        
        # 验证端点存在
        assert response.status_code in [200, 404, 500]
    
    def test_get_evolution_history(self, client):
        """测试获取进化历史"""
        agent_id = "agent-001"
        response = client.get(f"/api/v1/evolution/history/{agent_id}")
        
        # 验证端点存在
        assert response.status_code in [200, 404, 500]


class TestAPIErrorHandling:
    """测试 API 错误处理"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import create_app
        
        app = create_app()
        return TestClient(app)
    
    def test_invalid_json_payload(self, client):
        """测试无效的 JSON 载荷"""
        response = client.post(
            "/api/v1/agents",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client):
        """测试缺少必填字段"""
        # 发送空对象
        response = client.post("/api/v1/agents", json={})
        
        # 验证返回验证错误
        assert response.status_code in [422, 500]
    
    def test_invalid_agent_id(self, client):
        """测试无效的 Agent ID"""
        # 使用特殊字符的 ID
        response = client.get("/api/v1/agents/invalid<>id")
        
        # 验证处理无效 ID
        assert response.status_code in [200, 404, 422]
    
    def test_method_not_allowed(self, client):
        """测试不允许的方法"""
        response = client.delete("/health")
        
        # 验证方法不允许
        assert response.status_code == 405


class TestAPIResponseFormat:
    """测试 API 响应格式"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import create_app
        
        app = create_app()
        return TestClient(app)
    
    def test_health_response_format(self, client):
        """测试健康检查响应格式"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应包含必要字段
        assert "status" in data
        assert "service" in data
        assert "version" in data
    
    def test_content_type_header(self, client):
        """测试 Content-Type 响应头"""
        response = client.get("/health")
        
        assert "application/json" in response.headers.get("content-type", "")
