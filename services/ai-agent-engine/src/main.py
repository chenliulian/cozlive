"""
Cozlive AI Agent Engine
核心服务入口
"""

import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.routes import agent, chat, memory, evolution
from config.settings import settings
from core.memory.vector_store import VectorStore
from services.agent_manager import AgentManager
from utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动
    logger.info("Starting Cozlive AI Agent Engine...")
    
    # 初始化向量数据库
    app.state.vector_store = VectorStore()
    await app.state.vector_store.initialize()
    
    # 初始化 Agent 管理器
    app.state.agent_manager = AgentManager()
    await app.state.agent_manager.initialize()
    
    logger.info("AI Agent Engine started successfully")
    
    yield
    
    # 关闭
    logger.info("Shutting down AI Agent Engine...")
    await app.state.agent_manager.close()
    await app.state.vector_store.close()
    logger.info("AI Agent Engine stopped")


def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="Cozlive AI Agent Engine",
        description="AI Agent 核心引擎 - 提供人设一致性、情感计算、长效记忆、自主行为等能力",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # 路由
    app.include_router(agent.router, prefix="/api/v1/agents", tags=["Agent"])
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
    app.include_router(memory.router, prefix="/api/v1/memory", tags=["Memory"])
    app.include_router(evolution.router, prefix="/api/v1/evolution", tags=["Evolution"])
    
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return {
            "status": "healthy",
            "service": "ai-agent-engine",
            "version": "1.0.0"
        }
    
    @app.get("/")
    async def root():
        """根路由"""
        return {
            "name": "Cozlive AI Agent Engine",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
    )
