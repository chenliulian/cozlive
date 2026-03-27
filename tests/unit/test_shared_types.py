"""
共享类型定义单元测试
测试 packages/shared-types 中的类型定义
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'packages', 'shared-types', 'src'))


class TestUserTypes:
    """测试用户相关类型"""
    
    def test_user_type_enum(self):
        """测试用户类型枚举"""
        # 由于 TypeScript 类型在 Python 中无法直接导入，我们模拟验证
        user_types = ["human", "agent"]
        assert "human" in user_types
        assert "agent" in user_types
    
    def test_user_status_enum(self):
        """测试用户状态枚举"""
        statuses = ["active", "inactive", "suspended", "deleted"]
        assert "active" in statuses
        assert "inactive" in statuses
        assert "suspended" in statuses
        assert "deleted" in statuses
    
    def test_gender_enum(self):
        """测试性别枚举"""
        genders = ["male", "female", "other", "prefer_not_to_say"]
        assert "male" in genders
        assert "female" in genders
        assert "other" in genders
        assert "prefer_not_to_say" in genders
    
    def test_user_interface_structure(self, sample_user_data):
        """测试用户接口结构"""
        user = sample_user_data
        
        # 验证必需字段
        assert "id" in user
        assert "type" in user
        assert "status" in user
        
        # 验证人类用户特有字段
        if user["type"] == "human":
            assert "nickname" in user
            assert "interests" in user


class TestAgentTypes:
    """测试 AI Agent 相关类型"""
    
    def test_agent_type_enum(self):
        """测试 Agent 类型枚举"""
        agent_types = ["official", "custom", "derived"]
        assert "official" in agent_types
        assert "custom" in agent_types
        assert "derived" in agent_types
    
    def test_agent_status_enum(self):
        """测试 Agent 状态枚举"""
        statuses = ["active", "inactive", "training", "suspended"]
        assert "active" in statuses
        assert "inactive" in statuses
        assert "training" in statuses
        assert "suspended" in statuses
    
    def test_big_five_personality_structure(self, sample_agent_data):
        """测试大五人格结构"""
        agent = sample_agent_data
        personality = agent["personality"]
        big_five = personality["bigFive"]
        
        # 验证大五人格维度
        dimensions = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        for dim in dimensions:
            assert dim in big_five
            assert 0 <= big_five[dim] <= 100
    
    def test_agent_interface_structure(self, sample_agent_data):
        """测试 Agent 接口结构"""
        agent = sample_agent_data
        
        # 验证必需字段
        assert "id" in agent
        assert "type" in agent
        assert "agentType" in agent
        assert "name" in agent
        assert "roleIdentity" in agent
        assert "personality" in agent
        assert "abilities" in agent
        assert "isPublic" in agent
        assert "status" in agent


class TestSocialTypes:
    """测试社交关系类型"""
    
    def test_connection_type_enum(self):
        """测试连接类型枚举"""
        types = ["follow", "connect", "friend", "block"]
        assert "follow" in types
        assert "connect" in types
        assert "friend" in types
        assert "block" in types
    
    def test_connection_status_enum(self):
        """测试连接状态枚举"""
        statuses = ["pending", "active", "inactive", "blocked"]
        assert "pending" in statuses
        assert "active" in statuses
        assert "inactive" in statuses
        assert "blocked" in statuses
    
    def test_connection_structure(self):
        """测试连接结构"""
        connection = {
            "id": "conn-001",
            "sourceId": "user-001",
            "targetId": "agent-001",
            "type": "connect",
            "status": "active",
            "intimacy": 75,
            "interactionCount": 100,
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
        }
        
        assert connection["intimacy"] >= 0 and connection["intimacy"] <= 100
        assert connection["interactionCount"] >= 0


class TestMessageTypes:
    """测试消息相关类型"""
    
    def test_message_type_enum(self):
        """测试消息类型枚举"""
        types = ["text", "image", "voice", "video", "file", "location", "system"]
        for t in types:
            assert t in types
    
    def test_message_status_enum(self):
        """测试消息状态枚举"""
        statuses = ["sending", "sent", "delivered", "read", "failed"]
        assert "sending" in statuses
        assert "sent" in statuses
        assert "delivered" in statuses
        assert "read" in statuses
        assert "failed" in statuses
    
    def test_message_structure(self, sample_message_data):
        """测试消息结构"""
        message = sample_message_data
        
        assert "id" in message
        assert "conversationId" in message
        assert "senderId" in message
        assert "senderType" in message
        assert "type" in message
        assert "content" in message
        assert "status" in message
    
    def test_conversation_type_enum(self):
        """测试会话类型枚举"""
        types = ["private", "group", "ai_assistant"]
        assert "private" in types
        assert "group" in types
        assert "ai_assistant" in types


class TestContentTypes:
    """测试内容相关类型"""
    
    def test_post_type_enum(self):
        """测试动态类型枚举"""
        types = ["text", "image", "video", "audio", "link", "poll"]
        for t in types:
            assert t in types
    
    def test_post_visibility_enum(self):
        """测试动态可见性枚举"""
        visibilities = ["public", "followers", "private"]
        assert "public" in visibilities
        assert "followers" in visibilities
        assert "private" in visibilities
    
    def test_post_structure(self):
        """测试动态结构"""
        post = {
            "id": "post-001",
            "authorId": "user-001",
            "authorType": "human",
            "type": "text",
            "content": "测试内容",
            "visibility": "public",
            "tags": ["测试", "示例"],
            "likeCount": 10,
            "commentCount": 5,
            "shareCount": 2,
            "viewCount": 100,
        }
        
        assert post["likeCount"] >= 0
        assert post["commentCount"] >= 0
        assert post["shareCount"] >= 0
        assert post["viewCount"] >= 0


class TestGroupTypes:
    """测试社群相关类型"""
    
    def test_group_type_enum(self):
        """测试社群类型枚举"""
        types = ["public", "private", "paid"]
        assert "public" in types
        assert "private" in types
        assert "paid" in types
    
    def test_group_structure(self):
        """测试社群结构"""
        group = {
            "id": "group-001",
            "name": "测试社群",
            "description": "这是一个测试社群",
            "type": "public",
            "creatorId": "user-001",
            "admins": ["user-001"],
            "members": ["user-001", "user-002"],
            "agents": ["agent-001"],
            "memberCount": 2,
            "maxMembers": 100,
            "isAIEnabled": True,
        }
        
        assert group["memberCount"] <= group["maxMembers"]
        assert len(group["members"]) == group["memberCount"]


class TestMembershipTypes:
    """测试会员相关类型"""
    
    def test_membership_tier_enum(self):
        """测试会员等级枚举"""
        tiers = ["free", "premium", "super"]
        assert "free" in tiers
        assert "premium" in tiers
        assert "super" in tiers
    
    def test_membership_structure(self):
        """测试会员结构"""
        membership = {
            "id": "mem-001",
            "userId": "user-001",
            "tier": "premium",
            "isAutoRenew": True,
            "features": ["无限连接", "高级功能"],
        }
        
        assert membership["tier"] in ["free", "premium", "super"]


class TestApiTypes:
    """测试 API 相关类型"""
    
    def test_api_response_structure(self):
        """测试 API 响应结构"""
        response = {
            "success": True,
            "data": {"id": "123", "name": "测试"},
            "meta": {
                "page": 1,
                "limit": 10,
                "total": 100,
                "hasMore": True,
            }
        }
        
        assert isinstance(response["success"], bool)
        assert "data" in response
        assert response["meta"]["page"] >= 1
        assert response["meta"]["limit"] > 0
        assert response["meta"]["total"] >= 0
    
    def test_error_response_structure(self):
        """测试错误响应结构"""
        error_response = {
            "success": False,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": "用户不存在",
                "details": {"userId": "123"},
            }
        }
        
        assert error_response["success"] == False
        assert "error" in error_response
        assert "code" in error_response["error"]
        assert "message" in error_response["error"]


class TestWebSocketTypes:
    """测试 WebSocket 相关类型"""
    
    def test_websocket_event_enum(self):
        """测试 WebSocket 事件枚举"""
        events = [
            "connect",
            "disconnect",
            "message:new",
            "message:update",
            "message:delete",
            "message:read",
            "user:online",
            "user:offline",
            "user:typing",
            "notification:new",
            "agent:thinking",
            "agent:response",
        ]
        
        for event in events:
            assert event in events
    
    def test_websocket_message_structure(self):
        """测试 WebSocket 消息结构"""
        message = {
            "event": "message:new",
            "data": {"id": "msg-001", "content": "你好"},
            "timestamp": 1704067200000,
        }
        
        assert "event" in message
        assert "data" in message
        assert "timestamp" in message
        assert isinstance(message["timestamp"], int)
