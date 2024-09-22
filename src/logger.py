from loguru import logger
import sys


def configure_logger():
    # 清空默认的 logger 配置
    logger.remove()

    # 添加一个新的输出到控制台
    logger.add(sys.stderr, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO")

    # 可以选择添加一个文件输出
    logger.add("logs/{time}.log", rotation="1 day", retention="7 days", level="DEBUG",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


# 调用配置函数来设置 logger
configure_logger()
