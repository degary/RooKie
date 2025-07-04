"""
Loguru 日志使用示例
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logger import get_logger

# 获取logger实例
logger = get_logger()

def demo_logging():
    """演示各种日志级别的使用"""
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    logger.critical("这是严重错误")
    
    # 结构化日志 - 使用不同的参数名
    logger.info("用户登录", userId=123, clientIp="192.168.1.1")
    logger.info("订单创建", orderId="ORD001", amount=99.99, currency="USD")
    
    # 异常记录
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("发生除零错误")
    
    # 使用上下文管理器 - 可以使用任意参数名
    with logger.contextualize(requestId="REQ-abc123", userId=456, sessionId="sess_789"):
        logger.info("开始处理请求")
        logger.info("验证用户权限")
        logger.info("查询数据库")
        logger.info("请求处理完成")
    
    # 不同的上下文示例
    with logger.contextualize(traceId="trace-xyz", spanId="span-001"):
        logger.info("微服务调用")
        logger.info("返回结果")
    
    # 上下文外的日志不会包含上述信息
    logger.info("上下文外的普通日志")

if __name__ == "__main__":
    demo_logging()