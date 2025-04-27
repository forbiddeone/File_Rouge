from loguru import logger

logger.add("logs/main.log", rotation="500 KB", retention="10 days", level="INFO")
