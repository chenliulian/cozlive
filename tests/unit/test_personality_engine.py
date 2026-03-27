"""
人格一致性引擎单元测试
测试 AI Agent 人设一致性的核心功能
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# 添加服务路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'ai-agent-engine', 'src'))


class TestPersonalityProfile:
    """测试人格画像类"""
    
    def test_personality_profile_creation(self, sample_personality_profile):
        """测试人格画像创建"""
        profile = sample_personality_profile
        
        assert profile.agent_id == "test-agent-001"
        assert profile.name == "测试助手"
        assert profile.role_identity == "智能助手"
        assert profile.openness == 70
        assert profile.conscientiousness == 80
        assert profile.extraversion == 60
        assert profile.agreeableness == 75
        assert profile.neuroticism == 30
    
    def test_personality_profile_default_values(self):
        """测试人格画像默认值"""
        from core.personality.engine import PersonalityProfile
        
        profile = PersonalityProfile(
            agent_id="test-002",
            name="测试",
            role_identity="助手"
        )
        
        # 验证默认值
        assert profile.personality_traits == []
        assert profile.vocabulary_preference == []
        assert profile.sentence_patterns == []
        assert profile.abilities == []
        assert profile.preferred_topics == []
        assert profile.disliked_topics == []
        assert profile.active_hours == list(range(24))
    
    def test_personality_profile_to_dict(self, sample_personality_profile):
        """测试人格画像转换为字典"""
        profile = sample_personality_profile
        data = profile.to_dict()
        
        assert data["agent_id"] == "test-agent-001"
        assert data["name"] == "测试助手"
        assert "big_five" in data
        assert data["big_five"]["openness"] == 70
        assert "social_preferences" in data


class TestPersonalityEngine:
    """测试人格一致性引擎"""
    
    @pytest.fixture
    def engine(self):
        """创建引擎实例"""
        from core.personality.engine import PersonalityEngine
        return PersonalityEngine()
    
    def test_engine_initialization(self, engine):
        """测试引擎初始化"""
        assert engine is not None
        assert hasattr(engine, 'agents')
    
    def test_create_system_prompt(self, engine, sample_personality_profile):
        """测试系统提示词生成"""
        profile = sample_personality_profile
        prompt = engine._create_system_prompt(profile)
        
        # 验证提示词包含关键信息
        assert "测试助手" in prompt
        assert "智能助手" in prompt
        assert "友善" in prompt or "耐心" in prompt or "专业" in prompt
    
    def test_validate_response_consistency(self, engine, sample_personality_profile):
        """测试响应一致性验证"""
        profile = sample_personality_profile
        
        # 测试一致的响应
        consistent_response = "我很乐意帮助您解决这个问题。"
        is_valid, score = engine.validate_response_consistency(
            profile, consistent_response, "如何学习编程？"
        )
        
        assert isinstance(is_valid, bool)
        assert 0 <= score <= 1
    
    def test_get_speaking_style_guidance(self, engine, sample_personality_profile):
        """测试说话风格指导生成"""
        profile = sample_personality_profile
        guidance = engine._get_speaking_style_guidance(profile)
        
        assert isinstance(guidance, str)
        assert len(guidance) > 0
    
    def test_big_five_to_traits(self, engine):
        """测试大五人格转换为特质描述"""
        traits = engine._big_five_to_traits(
            openness=80,
            conscientiousness=70,
            extraversion=60,
            agreeableness=90,
            neuroticism=30
        )
        
        assert isinstance(traits, list)
        assert len(traits) > 0


class TestPersonalityConsistency:
    """测试人设一致性约束"""
    
    def test_role_identity_constraint(self, sample_personality_profile):
        """测试角色身份约束"""
        profile = sample_personality_profile
        
        # 验证角色身份不为空
        assert profile.role_identity is not None
        assert len(profile.role_identity) > 0
    
    def test_big_five_range_constraint(self, sample_personality_profile):
        """测试大五人格范围约束"""
        profile = sample_personality_profile
        
        # 验证所有维度在 0-100 范围内
        dimensions = [
            profile.openness,
            profile.conscientiousness,
            profile.extraversion,
            profile.agreeableness,
            profile.neuroticism,
        ]
        
        for dimension in dimensions:
            assert 0 <= dimension <= 100
    
    def test_active_hours_constraint(self, sample_personality_profile):
        """测试活跃时段约束"""
        profile = sample_personality_profile
        
        # 验证活跃时段在 0-23 范围内
        for hour in profile.active_hours:
            assert 0 <= hour <= 23
    
    @pytest.mark.parametrize("field,value", [
        ("openness", 50),
        ("conscientiousness", 60),
        ("extraversion", 70),
        ("agreeableness", 80),
        ("neuroticism", 40),
    ])
    def test_personality_dimension_update(self, sample_personality_profile, field, value):
        """测试人格维度更新"""
        profile = sample_personality_profile
        setattr(profile, field, value)
        assert getattr(profile, field) == value


class TestPersonalityEdgeCases:
    """测试人格引擎边界情况"""
    
    def test_empty_personality_traits(self):
        """测试空性格特质"""
        from core.personality.engine import PersonalityProfile
        
        profile = PersonalityProfile(
            agent_id="test-003",
            name="测试",
            role_identity="助手",
            personality_traits=[]
        )
        
        assert profile.personality_traits == []
    
    def test_extreme_big_five_values(self):
        """测试极端大五人格值"""
        from core.personality.engine import PersonalityProfile
        
        profile = PersonalityProfile(
            agent_id="test-004",
            name="极端性格",
            role_identity="测试",
            openness=0,
            conscientiousness=100,
            extraversion=0,
            agreeableness=100,
            neuroticism=0,
        )
        
        assert profile.openness == 0
        assert profile.conscientiousness == 100
    
    def test_long_backstory(self):
        """测试长背景故事"""
        from core.personality.engine import PersonalityProfile
        
        long_backstory = "这是一个很长的背景故事。" * 100
        profile = PersonalityProfile(
            agent_id="test-005",
            name="长故事",
            role_identity="测试",
            backstory=long_backstory
        )
        
        assert profile.backstory == long_backstory
