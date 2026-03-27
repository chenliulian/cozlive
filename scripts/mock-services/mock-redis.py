#!/usr/bin/env python3
"""
模拟 Redis 服务 - 用于测试
"""

import socket
import sys
from datetime import datetime

def main():
    PORT = 6379
    
    print(f"🔴 Mock Redis started on port {PORT}")
    print(f"   This is a mock service for development/testing only")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', PORT))
        sock.listen(5)
        
        while True:
            try:
                conn, addr = sock.accept()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Redis: Connection from {addr}")
                
                # 处理 Redis 命令
                data = conn.recv(1024)
                if data:
                    # 简单响应 +PONG
                    if b'PING' in data:
                        conn.send(b'+PONG\r\n')
                    else:
                        conn.send(b'+OK\r\n')
                
                conn.close()
                
            except Exception as e:
                print(f"Redis Error: {e}")
                
    except KeyboardInterrupt:
        print("\n👋 Mock Redis stopped")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
