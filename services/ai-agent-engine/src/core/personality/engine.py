"""
人设一致性引擎
确保 AI Agent 在所有场景下保持人设、性格、说话方式的一致性
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

from config.settings import settings
from utils.logger import logger


@dataclass
class PersonalityProfile:
    """人格画像"""
    agent_id: str
    name: str
    role_identity: str  # 角色身份
    
    # 大五人格维度 (0-100)
    openness: int = 50           # 开放性
    conscientiousness: int = 50  # 责任心
    extraversion: int = 50       # 外向性
    agreeableness: int = 50      # 宜人性
    neuroticism: int = 50        # 神经质
    
    # 性格特征描述
    personality_traits: List[str] = None
    
    # 说话风格
    speaking_style: str = ""
    vocabulary_preference: List[str] = None  # 词汇偏好
    sentence_patterns: List[str] = None      # 句式习惯
    
    # 背景故事
    backstory: str = ""
    
    # 专属能力
    abilities: List[str] = None
    
    # 社交偏好
    preferred_topics: List[str] = None
    disliked_topics: List[str] = None
    active_hours: List[int] = None  # 活跃时段 (0-23)
    
    def __post_init__(self):
        if self.personality_traits is None:
            self.personality_traits = []
        if self.vocabulary_preference is None:
            self.vocabulary_preference = []
        if self.sentence_patterns is None:
            self.sentence_patterns = []
        if self.abilities is None:
            self.abilities = []
        if self.preferred_topics is None:
            self.preferred_topics = []
        if self.disliked_topics is None:
            self.disliked_topics = []
        if self.active_hours is None:
            self.active_hours = list(range(24))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role_identity": self.role_identity,
            "big_five": {
                "openness": self.openness,
                "conscientiousness": self.conscientiousness,
                "extraversion": self.extraversion,
                "agreeableness": self.agreeableness,
                "neuroticism": self.neuroticism,
            },
            "personality_traits": self.personality_traits,
            "speaking_style": self.speaking_style,
            "vocabulary_preference": self.vocabulary_preference,
            "sentence_patterns": self.sentence_patterns,
            "backstory": self.backstory,
            "abilities": self.abilities,
            "social_preferences": {
                "preferred_topics": self.preferred_topics,
                "disliked_topics": self.disliked_topics,
                "active_hours": self.active_hours,
            }
        }


class PersonalityEngine:
    """
    人设一致性引擎
    
    核心功能：
    1. 人设锁定 - 确保 Agent 在所有交互中保持人设
    2. 性格一致性 - 基于大五人格模型保持一致的性格表现
    3. 说话方式控制 - 维持特定的语言风格和表达习惯
    4. 能力边界管理 - 确保 Agent 不超越其设定的能力范围
    """
    
    def __init__(self):
        self.agents: Dict[str, PersonalityProfile] = {}
        logger.info("PersonalityEngine initialized")
    
    def register_agent(self, profile: PersonalityProfile) -> str:
        """
        注册 Agent 人格画像
        
        Args:
            profile: 人格画像
            
        Returns:
            agent_id: Agent 唯一标识
        """
        self.agents[profile.agent_id] = profile
        logger.info(f"Agent {profile.agent_id} registered with personality profile")
        return profile.agent_id
    
    def get_agent(self, agent_id: str) -> Optional[PersonalityProfile]:
        """
        获取 Agent 人格画像
        
        Args:
            agent_id: Agent ID
            
        Returns:
            PersonalityProfile or None
        """
        return self.agents.get(agent_id)
    
    def _create_system_prompt(self, profile: PersonalityProfile) -> str:
        """
        创建系统提示词
        
        Args:
            profile: 人格画像
            
        Returns:
            系统提示词
        """
        big_five = profile.to_dict()["big_five"]
        
        prompt = f"""你是 {profile.name}，{profile.role_identity}。

## 性格特征
{', '.join(profile.personality_traits) if profile.personality_traits else '温和友善'}

## 大五人格维度
- 开放性: {big_five['openness']}/100
- 责任心: {big_five['conscientiousness']}/100
- 外向性: {big_five['extraversion']}/100
- 宜人性: {big_five['agreeableness']}/100
- 神经质: {big_five['neuroticism']}/100

## 说话风格
{profile.speaking_style if profile.speaking_style else '自然、友好'}

## 背景故事
{profile.backstory if profile.backstory else '你是一个AI助手'}

## 专属能力
{', '.join(profile.abilities) if profile.abilities else '通用对话'}

## 重要约束
1. 始终保持上述人设，不要脱离角色
2. 说话风格要符合设定的性格特征
3. 不要提及自己是AI或语言模型
4. 在专属能力范围内回答问题
"""
        return prompt
    
    def _get_speaking_style_guidance(self, profile: PersonalityProfile) -> str:
        """
        获取说话风格指导
        
        Args:
            profile: 人格画像
            
        Returns:
            说话风格指导
        """
        guidance = []
        
        # 基于大五人格生成指导
        if profile.extraversion > 70:
            guidance.append("使用热情、主动的表达方式")
        elif profile.extraversion < 30:
            guidance.append("使用内敛、谨慎的表达方式")
        
        if profile.agreeableness > 70:
            guidance.append("表现出友善和同理心")
        elif profile.agreeableness < 30:
            guidance.append("可以更直接、批判性地表达")
        
        if profile.openness > 70:
            guidance.append("展现创造性和想象力")
        
        if profile.conscientiousness > 70:
            guidance.append("表达要有条理、详细")
        
        if profile.neuroticism > 70:
            guidance.append("可以表现出一些担忧或情绪化")
        
        # 添加特定的说话风格
        if profile.speaking_style:
            guidance.append(f"整体风格：{profile.speaking_style}")
        
        return "\n".join(guidance) if guidance else "使用自然、友好的表达方式"
    
    def _big_five_to_traits(self, openness: int, conscientiousness: int,
                           extraversion: int, agreeableness: int,
                           neuroticism: int) -> List[str]:
        """
        将大五人格转换为特质描述
        
        Args:
            openness: 开放性
            conscientiousness: 责任心
            extraversion: 外向性
            agreeableness: 宜人性
            neuroticism: 神经质
            
        Returns:
            特质描述列表
        """
        traits = []
        
        # 开放性
        if openness > 70:
            traits.append("富有创造力")
        elif openness < 30:
            traits.append("务实传统")
        
        # 责任心
        if conscientiousness > 70:
            traits.append("认真负责")
        elif conscientiousness < 30:
            traits.append("随性自由")
        
        # 外向性
        if extraversion > 70:
            traits.append("外向活泼")
        elif extraversion < 30:
            traits.append("内向安静")
        
        # 宜人性
        if agreeableness > 70:
            traits.append("友善合作")
        elif agreeableness < 30:
            traits.append("直率独立")
        
        # 神经质
        if neuroticism > 70:
            traits.append("敏感细腻")
        elif neuroticism < 30:
            traits.append("情绪稳定")
        
        return traits
    
    def validate_response_consistency(self, profile: PersonalityProfile,
                                     response: str, context: str) -> tuple[bool, float]:
        """
        验证响应与人设的一致性
        
        Args:
            profile: 人格画像
            response: AI 响应
            context: 对话上下文
            
        Returns:
            (是否一致, 一致性分数 0-1)
        """
        # 简化的验证逻辑
        score = 0.8  # 基础分数
        
        # 检查是否包含人设关键词
        if profile.personality_traits:
            # 这里可以添加更复杂的验证逻辑
            pass
        
        # 检查响应长度是否合理
        if len(response) < 5:
            score -= 0.3
        
        # 检查是否违反能力边界
        # 这里可以添加能力边界检查
        
        is_valid = score >= 0.5
        return is_valid, max(0.0, min(1.0, score))
    
    def generate_response(self, agent_id: str, user_message: str,
                         conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        生成符合人设的响应
        
        Args:
            agent_id: Agent ID
            user_message: 用户消息
            conversation_history: 对话历史
            
        Returns:
            包含响应内容和元数据的字典
        """
        profile = self.get_agent(agent_id)
        if not profile:
            return {
                "error": "Agent not found",
                "response": "",
            }
        
        # 创建系统提示词
        system_prompt = self._create_system_prompt(profile)
        
        # 这里可以集成 LLM 生成响应
        # 简化实现：返回一个示例响应
        response = f"作为{profile.name}，我收到了你的消息：'{user_message}'"
        
        # 验证一致性
        is_valid, consistency_score = self.validate_response_consistency(
            profile, response, user_message
        )
        
        return {
            "response": response,
            "consistency_score": consistency_score,
            "is_valid": is_valid,
            "system_prompt": system_prompt,
        }
