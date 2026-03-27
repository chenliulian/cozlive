#!/usr/bin/env python3
"""
模拟用户服务 - 用于测试项目结构
"""

import json
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 3001

class UserServiceHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] User Service: {format % args}")
    
    def _send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self._send_json_response({
                "status": "healthy",
                "service": "user-service",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            })
        elif self.path == '/api/v1/users':
            self._send_json_response({
                "success": True,
                "data": [
                    {
                        "id": "user_001",
                        "nickname": "测试用户1",
                        "email": "user1@cozlive.com",
                        "type": "human",
                        "status": "active"
                    },
                    {
                        "id": "user_002",
                        "nickname": "测试用户2",
                        "email": "user2@cozlive.com",
                        "type": "human",
                        "status": "active"
                    }
                ]
            })
        elif self.path.startswith('/api/v1/users/'):
            user_id = self.path.split('/')[-1]
            self._send_json_response({
                "success": True,
                "data": {
                    "id": user_id,
                    "nickname": f"用户_{user_id}",
                    "email": f"{user_id}@cozlive.com",
                    "type": "human",
                    "status": "active",
                    "createdAt": datetime.now().isoformat()
                }
            })
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
        
        if self.path == '/api/v1/auth/login':
            self._send_json_response({
                "success": True,
                "data": {
                    "accessToken": "mock_access_token_12345",
                    "refreshToken": "mock_refresh_token_67890",
                    "user": {
                        "id": "user_001",
                        "nickname": data.get('email', 'user').split('@')[0],
                        "email": data.get('email', 'user@cozlive.com'),
                        "type": "human"
                    }
                }
            })
        elif self.path == '/api/v1/auth/register':
            self._send_json_response({
                "success": True,
                "data": {
                    "id": f"user_{datetime.now().strftime('%s')}",
                    "nickname": data.get('nickname', '新用户'),
                    "email": data.get('email'),
                    "type": "human",
                    "status": "active",
                    "createdAt": datetime.now().isoformat()
                }
            }, 201)
        else:
            self._send_json_response({
                "success": True,
                "data": {
                    "message": "Operation successful",
                    "received": data
                }
            })
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def main():
    server = HTTPServer(('0.0.0.0', PORT), UserServiceHandler)
    print(f"🚀 User Service started on port {PORT}")
    print(f"   Health check: http://localhost:{PORT}/health")
    print(f"   API docs: http://localhost:{PORT}/api/docs")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 User Service stopped")
        sys.exit(0)

if __name__ == '__main__':
    main()
