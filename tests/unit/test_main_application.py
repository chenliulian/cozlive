"""
主应用单元测试
测试 AI Agent Engine 的 FastAPI 应用
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'ai-agent-engine', 'src'))


class TestApplication:
    """测试应用创建"""
    
    def test_create_app(self):
        """测试应用创建函数"""
        from main import create_app
        from fastapi import FastAPI
        
        app = create_app()
        
        assert isinstance(app, FastAPI)
        assert app.title == "Cozlive AI Agent Engine"
        assert app.version == "1.0.0"
    
    def test_app_routers(self):
        """测试应用路由注册"""
        from main import create_app
        
        app = create_app()
        
        # 验证路由前缀
        routes = [route.path for route in app.routes]
        
        # 检查主要路由是否存在
        assert any("/api/v1/agents" in route for route in routes if isinstance(route, str))
        assert any("/api/v1/chat" in route for route in routes if isinstance(route, str))
        assert any("/api/v1/memory" in route for route in routes if isinstance(route, str))
        assert any("/api/v1/evolution" in route for route in routes if isinstance(route, str))
    
    def test_health_endpoint(self):
        """测试健康检查端点"""
        from main import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ai-agent-engine"
        assert data["version"] == "1.0.0"
    
    def test_root_endpoint(self):
        """测试根端点"""
        from main import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Cozlive AI Agent Engine"
        assert "docs" in data


class TestMiddleware:
    """测试中间件"""
    
    def test_cors_middleware(self):
        """测试 CORS 中间件"""
        from main import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        # 测试 CORS 预检请求
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        
        assert response.status_code == 200
    
    def test_gzip_middleware(self):
        """测试 GZip 压缩中间件"""
        from main import create_app
        
        app = create_app()
        
        # 验证中间件存在
        middleware_classes = [type(m).__name__ for m in app.user_middleware]
        assert "GZipMiddleware" in middleware_classes or any("GZip" in str(m) for m in app.user_middleware)


class TestLifespan:
    """测试应用生命周期"""
    
    @pytest.mark.asyncio
    async def test_lifespan_startup(self):
        """测试生命周期启动"""
        from main import lifespan
        from fastapi import FastAPI
        
        app = FastAPI()
        
        with patch('main.VectorStore') as mock_vector_store, \
             patch('main.AgentManager') as mock_agent_manager:
            
            mock_vector_store_instance = AsyncMock()
            mock_agent_manager_instance = AsyncMock()
            
            mock_vector_store.return_value = mock_vector_store_instance
            mock_agent_manager.return_value = mock_agent_manager_instance
            
            async with lifespan(app) as context:
                # 验证初始化被调用
                mock_vector_store_instance.initialize.assert_called_once()
                mock_agent_manager_instance.initialize.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_shutdown(self):
        """测试生命周期关闭"""
        from main import lifespan
        from fastapi import FastAPI
        
        app = FastAPI()
        
        with patch('main.VectorStore') as mock_vector_store, \
             patch('main.AgentManager') as mock_agent_manager:
            
            mock_vector_store_instance = AsyncMock()
            mock_agent_manager_instance = AsyncMock()
            
            mock_vector_store.return_value = mock_vector_store_instance
            mock_agent_manager.return_value = mock_agent_manager_instance
            
            async with lifespan(app) as context:
                pass
            
            # 验证关闭被调用
            mock_agent_manager_instance.close.assert_called_once()
            mock_vector_store_instance.close.assert_called_once()


class TestAppState:
    """测试应用状态"""
    
    def test_app_state_initialization(self):
        """测试应用状态初始化"""
        from main import create_app
        
        app = create_app()
        
        # 验证应用状态属性存在
        assert hasattr(app, 'state')


class TestDocumentation:
    """测试 API 文档"""
    
    def test_docs_endpoint(self):
        """测试 Swagger 文档端点"""
        from main import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/docs")
        
        # Swagger UI 应该返回 HTML
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_redoc_endpoint(self):
        """测试 ReDoc 文档端点"""
        from main import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/redoc")
        
        # ReDoc 应该返回 HTML
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_openapi_schema(self):
        """测试 OpenAPI  schema"""
        from main import create_app
        from fastapi.testclient import TestClient
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "Cozlive AI Agent Engine"
        assert schema["info"]["version"] == "1.0.0"
