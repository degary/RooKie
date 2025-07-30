"""
响应装饰器
"""
from functools import wraps

from rest_framework.response import Response

from .wrapper import ApiResponse


def api_response(func):
    """
    API响应装饰器
    自动包装函数返回值为标准API响应格式
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            # 如果已经是ApiResponse对象，直接返回
            if isinstance(result, ApiResponse):
                return result.to_response()

            # 如果是DRF Response对象，不处理
            if isinstance(result, Response):
                return result

            # 包装普通返回值
            if isinstance(result, dict):
                return ApiResponse.success(data=result).to_response()
            elif isinstance(result, (list, tuple)):
                return ApiResponse.success(data=result).to_response()
            else:
                return ApiResponse.success(data=result).to_response()

        except Exception as e:
            # 异常会被全局异常处理器处理
            raise e

    return wrapper


def function_response(func):
    """
    函数响应装饰器
    用于普通函数，返回ApiResponse对象
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            # 如果已经是ApiResponse对象，直接返回
            if isinstance(result, ApiResponse):
                return result

            # 包装普通返回值
            return ApiResponse.success(data=result)

        except Exception as e:
            return ApiResponse.internal_error(f"函数执行失败: {str(e)}")

    return wrapper
