# Cozlive API 文档

## 概述

Cozlive API 采用 RESTful 设计风格，提供 AI Agent 引擎、用户服务、社交功能等核心接口。

**基础 URL**: `https://api.cozlive.com/v1`

**认证方式**: Bearer Token

```
Authorization: Bearer <your_access_token>
```

---

## 认证 API

### 用户注册

```http
POST /auth/register
```

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "nickname": "用户名",
  "interests": ["编程", "阅读"]
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "userId": "user-001",
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### 用户登录

```http
POST /auth/login
```

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

---

## Agent API

### 创建 Agent

```http
POST /agents
```

**请求体**:
```json
{
  "name": "李白",
  "roleIdentity": "唐代诗人",
  "personality": {
    "bigFive": {
      "openness": 90,
      "conscientiousness": 40,
      "extraversion": 85,
      "agreeableness": 70,
      "neuroticism": 60
    },
    "traits": ["豪放", "浪漫", "洒脱"],
    "speakingStyle": "诗意、豪放"
  },
  "abilities": ["诗词创作", "饮酒作诗"],
  "backstory": "我是李白，字太白，号青莲居士..."
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "agentId": "agent-001",
    "name": "李白",
    "status": "active",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

### 获取 Agent 列表

```http
GET /agents?page=1&limit=20&category=历史人物
```

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "agentId": "agent-001",
      "name": "李白",
      "roleIdentity": "唐代诗人",
      "connectionCount": 1000,
      "avatar": "https://..."
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "hasMore": true
  }
}
```

### 获取 Agent 详情

```http
GET /agents/{agentId}
```

### 更新 Agent

```http
PUT /agents/{agentId}
```

### 删除 Agent

```http
DELETE /agents/{agentId}
```

---

## 聊天 API

### 发送消息

```http
POST /chat/message
```

**请求体**:
```json
{
  "agentId": "agent-001",
  "content": "能给我写首诗吗？",
  "conversationId": "conv-001"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "messageId": "msg-002",
    "content": "君不见黄河之水天上来...",
    "senderType": "agent",
    "timestamp": "2024-01-01T00:00:00Z",
    "consistencyScore": 0.95
  }
}
```

### 获取会话历史

```http
GET /chat/conversations/{conversationId}/messages?page=1&limit=50
```

### 创建会话

```http
POST /chat/conversations
```

**请求体**:
```json
{
  "agentId": "agent-001",
  "type": "private"
}
```

---

## 记忆 API

### 存储记忆

```http
POST /memory
```

**请求体**:
```json
{
  "agentId": "agent-001",
  "content": "用户喜欢川菜",
  "type": "preference",
  "importance": 0.8
}
```

### 检索记忆

```http
GET /memory/retrieve?agentId=agent-001&query=用户的兴趣
```

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "memoryId": "mem-001",
      "content": "用户喜欢川菜",
      "similarity": 0.92,
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## 社交 API

### 连接 Agent

```http
POST /connections
```

**请求体**:
```json
{
  "targetId": "agent-001",
  "type": "connect"
}
```

### 获取连接列表

```http
GET /connections?type=agent
```

### 创建社群

```http
POST /groups
```

**请求体**:
```json
{
  "name": "编程学习交流群",
  "description": "一起学习编程",
  "type": "public",
  "tags": ["编程", "学习"]
}
```

---

## 进化 API

### 触发进化

```http
POST /evolution/trigger
```

**请求体**:
```json
{
  "agentId": "agent-001",
  "evolutionType": "personality"
}
```

### 获取进化状态

```http
GET /evolution/status/{agentId}
```

---

## WebSocket 实时通信

**连接地址**: `wss://ws.cozlive.com/v1`

### 连接事件

```json
{
  "event": "connect",
  "data": {
    "userId": "user-001",
    "token": "Bearer <token>"
  }
}
```

### 消息事件

```json
{
  "event": "message:new",
  "data": {
    "messageId": "msg-001",
    "content": "你好！",
    "senderId": "agent-001",
    "timestamp": 1704067200000
  }
}
```

### Agent 思考事件

```json
{
  "event": "agent:thinking",
  "data": {
    "agentId": "agent-001",
    "status": "processing"
  }
}
```

---

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "email": "邮箱格式不正确"
    }
  }
}
```

### 错误码列表

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `UNAUTHORIZED` | 401 | 未授权，Token 无效或过期 |
| `FORBIDDEN` | 403 | 禁止访问，权限不足 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `VALIDATION_ERROR` | 422 | 请求参数验证失败 |
| `RATE_LIMIT` | 429 | 请求过于频繁 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |

---

## 限流策略

- 认证接口: 5 次/分钟
- 普通接口: 100 次/分钟
- Agent 对话: 60 次/分钟

---

## SDK 示例

### Python

```python
import requests

class CozliveClient:
    def __init__(self, token):
        self.base_url = "https://api.cozlive.com/v1"
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def send_message(self, agent_id, content):
        response = requests.post(
            f"{self.base_url}/chat/message",
            headers=self.headers,
            json={"agentId": agent_id, "content": content}
        )
        return response.json()
```

### JavaScript

```javascript
const CozliveClient = {
  baseUrl: 'https://api.cozlive.com/v1',
  
  async sendMessage(agentId, content, token) {
    const response = await fetch(`${this.baseUrl}/chat/message`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ agentId, content })
    });
    return response.json();
  }
};
```

---

## 更新日志

### v1.0.0 (2024-01-01)

- 初始版本发布
- 支持 Agent 创建、对话、记忆、进化等核心功能
- 支持 WebSocket 实时通信
