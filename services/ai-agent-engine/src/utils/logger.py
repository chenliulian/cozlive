"""
日志工具
"""
import logging

# 创建日志记录器
logger = logging.getLogger("cozlive")
logger.setLevel(logging.INFO)

# 添加控制台处理器
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# 设置格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

logger.addHandler(handler)
