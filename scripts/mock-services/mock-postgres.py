#!/usr/bin/env python3
"""
模拟 PostgreSQL 服务 - 用于测试
"""

import socket
import sys
from datetime import datetime

def main():
    PORT = 5432
    
    print(f"🐘 Mock PostgreSQL started on port {PORT}")
    print(f"   This is a mock service for development/testing only")
    
    # 创建一个简单的 TCP 监听
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', PORT))
        sock.listen(5)
        
        while True:
            try:
                conn, addr = sock.accept()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] PostgreSQL: Connection from {addr}")
                
                # 发送 PostgreSQL 协议握手
                # PostgreSQL protocol version 3.0
                response = b'R\x00\x00\x00\x08\x00\x00\x00\x03'  # Authentication OK
                conn.send(response)
                conn.close()
                
            except Exception as e:
                print(f"PostgreSQL Error: {e}")
                
    except KeyboardInterrupt:
        print("\n👋 Mock PostgreSQL stopped")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
