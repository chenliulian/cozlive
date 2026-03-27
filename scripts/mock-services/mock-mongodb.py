#!/usr/bin/env python3
"""
模拟 MongoDB 服务 - 用于测试
"""

import socket
import sys
from datetime import datetime

def main():
    PORT = 27017
    
    print(f"🍃 Mock MongoDB started on port {PORT}")
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
                print(f"[{timestamp}] MongoDB: Connection from {addr}")
                
                # MongoDB wire protocol response
                # Simple hello response
                response = bytes([
                    0x5c, 0x00, 0x00, 0x00,  # message length
                    0x01, 0x00, 0x00, 0x00,  # request ID
                    0x00, 0x00, 0x00, 0x00,  # response to
                    0xdd, 0x07, 0x00, 0x00,  # opcode (OP_MSG)
                    0x00, 0x00, 0x00, 0x00,  # flag bits
                    0x00,                    # sections kind
                ])
                conn.send(response)
                conn.close()
                
            except Exception as e:
                print(f"MongoDB Error: {e}")
                
    except KeyboardInterrupt:
        print("\n👋 Mock MongoDB stopped")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
