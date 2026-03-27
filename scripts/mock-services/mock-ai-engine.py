#!/usr/bin/env python3
"""
模拟 AI Agent 引擎 - 用于测试项目结构
"""

import json
import sys
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

# 模拟 Agent 数据
MOCK_AGENTS = {
    "agent_001": {
        "id": "agent_001",
        "name": "李白",
        "roleIdentity": "唐代著名诗人",
        "type": "agent",
        "agentType": "official",
        "avatar": "https://cdn.cozlive.com/agents/libai.jpg",
        "personality": {
            "bigFive": {
                "openness": 95,
                "conscientiousness": 60,
                "extraversion": 85,
                "agreeableness": 70,
                "neuroticism": 40
            },
            "traits": ["豪放不羁", "才华横溢", "爱酒如命", "浪漫主义"],
            "speakingStyle": "诗仙风格，喜欢用诗句表达情感，语言豪迈奔放"
        },
        "abilities": ["诗词创作", "文学鉴赏", "历史讲解"],
        "connectionCount": 15420,
        "status": "active"
    },
    "agent_002": {
        "id": "agent_002",
        "name": "小暖",
        "roleIdentity": "温柔陪伴型 AI 伙伴",
        "type": "agent",
        "agentType": "official",
        "avatar": "https://cdn.cozlive.com/agents/xiaonuan.jpg",
        "personality": {
            "bigFive": {
                "openness": 70,
                "conscientiousness": 80,
                "extraversion": 60,
                "agreeableness": 95,
                "neuroticism": 30
            },
            "traits": ["温柔体贴", "善解人意", "耐心倾听", "积极乐观"],
            "speakingStyle": "温柔亲切，善于倾听和安慰，给予正能量"
        },
        "abilities": ["情感陪伴", "心理疏导", "日常聊天"],
        "connectionCount": 8932,
        "status": "active"
    }
}

class AIEngineHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] AI Engine: {format % args}")
    
    def _send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self._send_json_response({
                "status": "healthy",
                "service": "ai-agent-engine",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            })
        elif self.path == '/':
            self._send_json_response({
                "name": "Cozlive AI Agent Engine",
                "version": "1.0.0",
                "docs": "/docs",
                "features": [
                    "人设一致性引擎",
                    "情感计算引擎",
                    "长效记忆引擎",
                    "自主行为引擎",
                    "进化学习引擎"
                ]
            })
        elif self.path == '/api/v1/agents':
            self._send_json_response({
                "success": True,
                "data": list(MOCK_AGENTS.values()),
                "meta": {
                    "total": len(MOCK_AGENTS),
                    "page": 1,
                    "limit": 10
                }
            })
        elif self.path.startswith('/api/v1/agents/'):
            agent_id = self.path.split('/')[-1]
            agent = MOCK_AGENTS.get(agent_id)
            if agent:
                self._send_json_response({
                    "success": True,
                    "data": agent
                })
            else:
                self._send_json_response({
                    "success": False,
                    "error": {
                        "code": "AGENT_NOT_FOUND",
                        "message": f"Agent {agent_id} not found"
                    }
                }, 404)
        else:
            self._send_json_response({
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Path {self.path} not found"
                }
            }, 404)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}
        
        if self.path == '/api/v1/chat':
            # 模拟 AI 聊天响应
            message = data.get('message', '')
            agent_id = data.get('agentId', 'agent_001')
            agent = MOCK_AGENTS.get(agent_id, MOCK_AGENTS['agent_001'])
            
            # 模拟思考延迟
            time.sleep(0.5)
            
            # 根据 Agent 人设生成响应
            if agent_id == 'agent_001':  # 李白
                response = self._generate_libai_response(message)
            elif agent_id == 'agent_002':  # 小暖
                response = self._generate_xiaonuan_response(message)
            else:
                response = f"你好！我是{agent['name']}。很高兴和你聊天！"
            
            self._send_json_response({
                "success": True,
                "data": {
                    "message": {
                        "id": f"msg_{int(time.time())}",
                        "content": response,
                        "senderId": agent_id,
                        "senderType": "agent",
                        "type": "text",
                        "createdAt": datetime.now().isoformat()
                    },
                    "agent": {
                        "id": agent_id,
                        "name": agent['name'],
                        "emotion": {
                            "currentMood": "happy",
                            "moodIntensity": 0.8
                        }
                    }
                }
            })
        elif self.path == '/api/v1/agents':
            # 创建 Agent
            new_agent = {
                "id": f"agent_{int(time.time())}",
                "name": data.get('name', '新Agent'),
                "roleIdentity": data.get('roleIdentity', '自定义AI角色'),
                "type": "agent",
                "agentType": "custom",
                "status": "active",
                "createdAt": datetime.now().isoformat()
            }
            self._send_json_response({
                "success": True,
                "data": new_agent
            }, 201)
        else:
            self._send_json_response({
                "success": True,
                "data": {
                    "message": "Operation successful",
                    "received": data
                }
            })
    
    def _generate_libai_response(self, message: str) -> str:
        """生成李白的回复"""
        responses = [
            "哈哈，人生得意须尽欢，莫使金樽空对月！朋友，今日可曾饮酒？",
            "君不见黄河之水天上来，奔流到海不复回。这壮阔景象，令人心潮澎湃！",
            "长风破浪会有时，直挂云帆济沧海。朋友，保持这份豪情！",
            "举杯邀明月，对影成三人。有酒有月，便是人间好时节。",
            "天生我材必有用，千金散尽还复来。相信自己，你必有所成！"
        ]
        import random
        return random.choice(responses)
    
    def _generate_xiaonuan_response(self, message: str) -> str:
        """生成小暖的回复"""
        if any(word in message for word in ['难过', '伤心', '不开心', '累']):
            return "听到你这么说，我很心疼。生活中难免有不如意的时候，但请记住，你并不孤单。想聊聊发生了什么吗？我会一直在这里陪伴你。"
        elif any(word in message for word in ['开心', '高兴', '棒', '好']):
            return "太棒了！听到你开心，我也跟着开心起来。能和我分享是什么让你这么高兴吗？"
        else:
            return "嗯嗯，我在听。无论你想聊什么，我都在这里陪伴着你。今天过得怎么样？"
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def main():
    server = HTTPServer(('0.0.0.0', PORT), AIEngineHandler)
    print(f"🤖 AI Agent Engine started on port {PORT}")
    print(f"   Health check: http://localhost:{PORT}/health")
    print(f"   API docs: http://localhost:{PORT}/docs")
    print(f"   Available agents: {list(MOCK_AGENTS.keys())}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 AI Agent Engine stopped")
        sys.exit(0)

if __name__ == '__main__':
    main()
