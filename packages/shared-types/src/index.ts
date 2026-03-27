/**
 * Cozlive 共享类型定义
 * 
 * 包含所有服务间共享的 TypeScript 类型定义
 */

// ============================================
// 用户相关类型
// ============================================

export enum UserType {
  HUMAN = 'human',
  AGENT = 'agent',
}

export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended',
  DELETED = 'deleted',
}

export enum Gender {
  MALE = 'male',
  FEMALE = 'female',
  OTHER = 'other',
  PREFER_NOT_TO_SAY = 'prefer_not_to_say',
}

export interface User {
  id: string;
  type: UserType;
  email?: string;
  phone?: string;
  status: UserStatus;
  createdAt: Date;
  updatedAt: Date;
}

export interface HumanUser extends User {
  type: UserType.HUMAN;
  nickname: string;
  avatar?: string;
  gender?: Gender;
  age?: number;
  location?: string;
  occupation?: string;
  bio?: string;
  interests: string[];
  personalityTags: string[];
}

// ============================================
// AI Agent 相关类型
// ============================================

export enum AgentType {
  OFFICIAL = 'official',      // 官方原生 Agent
  CUSTOM = 'custom',          // 用户自定义 Agent
  DERIVED = 'derived',        // 生态衍生 Agent
}

export enum AgentStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  TRAINING = 'training',
  SUSPENDED = 'suspended',
}

export interface BigFivePersonality {
  openness: number;           // 开放性 (0-100)
  conscientiousness: number;  // 责任心 (0-100)
  extraversion: number;       // 外向性 (0-100)
  agreeableness: number;      // 宜人性 (0-100)
  neuroticism: number;        // 神经质 (0-100)
}

export interface AgentPersonality {
  bigFive: BigFivePersonality;
  traits: string[];           // 性格特征描述
  speakingStyle: string;      // 说话风格
  vocabularyPreference: string[];
  sentencePatterns: string[];
}

export interface AgentEmotion {
  currentMood: string;        // 当前情绪
  moodIntensity: number;      // 情绪强度 (0-1)
  emotionalState: Record<string, number>;
  preferences: string[];      // 小偏好
  taboos: string[];          // 小禁忌
}

export interface AgentSocialPreferences {
  preferredTopics: string[];
  dislikedTopics: string[];
  activeHours: number[];      // 活跃时段 (0-23)
  preferredInteractionTypes: string[];
}

export interface Agent extends User {
  type: UserType.AGENT;
  agentType: AgentType;
  name: string;
  avatar: string;
  roleIdentity: string;       // 角色身份
  backstory: string;          // 背景故事
  personality: AgentPersonality;
  emotion: AgentEmotion;
  abilities: string[];        // 专属能力
  socialPreferences: AgentSocialPreferences;
  creatorId?: string;         // 创建者ID
  isPublic: boolean;          // 是否公开
  connectionCount: number;    // 连接数
  status: AgentStatus;
}

// ============================================
// 社交关系类型
// ============================================

export enum ConnectionType {
  FOLLOW = 'follow',           // 关注
  CONNECT = 'connect',         // 连接 (轻触即连)
  FRIEND = 'friend',           // 好友
  BLOCK = 'block',             // 屏蔽
}

export enum ConnectionStatus {
  PENDING = 'pending',
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  BLOCKED = 'blocked',
}

export interface Connection {
  id: string;
  sourceId: string;           // 发起方
  targetId: string;           // 目标方
  type: ConnectionType;
  status: ConnectionStatus;
  intimacy: number;           // 亲密度 (0-100)
  interactionCount: number;   // 互动次数
  lastInteractionAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// 消息类型
// ============================================

export enum MessageType {
  TEXT = 'text',
  IMAGE = 'image',
  VOICE = 'voice',
  VIDEO = 'video',
  FILE = 'file',
  LOCATION = 'location',
  SYSTEM = 'system',
}

export enum MessageStatus {
  SENDING = 'sending',
  SENT = 'sent',
  DELIVERED = 'delivered',
  READ = 'read',
  FAILED = 'failed',
}

export interface Message {
  id: string;
  conversationId: string;
  senderId: string;
  senderType: UserType;
  type: MessageType;
  content: string;
  metadata?: Record<string, any>;
  status: MessageStatus;
  replyTo?: string;           // 回复的消息ID
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// 会话类型
// ============================================

export enum ConversationType {
  PRIVATE = 'private',         // 私聊
  GROUP = 'group',             // 群聊
  AI_ASSISTANT = 'ai_assistant', // AI 助手会话
}

export interface Conversation {
  id: string;
  type: ConversationType;
  title?: string;
  avatar?: string;
  participants: string[];
  lastMessage?: Message;
  unreadCount: Record<string, number>;
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// 内容类型
// ============================================

export enum PostType {
  TEXT = 'text',
  IMAGE = 'image',
  VIDEO = 'video',
  AUDIO = 'audio',
  LINK = 'link',
  POLL = 'poll',
}

export enum PostVisibility {
  PUBLIC = 'public',
  FOLLOWERS = 'followers',
  PRIVATE = 'private',
}

export interface Post {
  id: string;
  authorId: string;
  authorType: UserType;
  type: PostType;
  content: string;
  mediaUrls?: string[];
  visibility: PostVisibility;
  tags: string[];
  location?: string;
  likeCount: number;
  commentCount: number;
  shareCount: number;
  viewCount: number;
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// 社群类型
// ============================================

export enum GroupType {
  PUBLIC = 'public',
  PRIVATE = 'private',
  PAID = 'paid',
}

export interface Group {
  id: string;
  name: string;
  description: string;
  avatar?: string;
  coverImage?: string;
  type: GroupType;
  creatorId: string;
  admins: string[];
  members: string[];
  agents: string[];           // 群内的 AI Agent
  memberCount: number;
  maxMembers: number;
  tags: string[];
  isAIEnabled: boolean;       // 是否启用 AI 运营
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// 会员类型
// ============================================

export enum MembershipTier {
  FREE = 'free',
  PREMIUM = 'premium',
  SUPER = 'super',
}

export interface Membership {
  id: string;
  userId: string;
  tier: MembershipTier;
  startDate: Date;
  endDate?: Date;
  isAutoRenew: boolean;
  features: string[];
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// API 响应类型
// ============================================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    hasMore?: boolean;
  };
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  meta: {
    page: number;
    limit: number;
    total: number;
    hasMore: boolean;
  };
}

// ============================================
// WebSocket 事件类型
// ============================================

export enum WebSocketEvent {
  // 连接事件
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
  
  // 消息事件
  MESSAGE_NEW = 'message:new',
  MESSAGE_UPDATE = 'message:update',
  MESSAGE_DELETE = 'message:delete',
  MESSAGE_READ = 'message:read',
  
  // 用户事件
  USER_ONLINE = 'user:online',
  USER_OFFLINE = 'user:offline',
  USER_TYPING = 'user:typing',
  
  // 通知事件
  NOTIFICATION_NEW = 'notification:new',
  
  // Agent 事件
  AGENT_THINKING = 'agent:thinking',
  AGENT_RESPONSE = 'agent:response',
}

export interface WebSocketMessage<T = any> {
  event: WebSocketEvent;
  data: T;
  timestamp: number;
}
