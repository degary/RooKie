"""
自定义异常类
"""
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .wrapper import ApiResponse, ErrorCode


class ApiException(Exception):
    """API异常基类"""

    def __init__(self, message: str, code: int = ErrorCode.OPERATION_FAILED, data=None):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(message)


class ValidationException(ApiException):
    """数据验证异常"""

    def __init__(self, message: str = "数据验证失败", data=None):
        super().__init__(message, ErrorCode.VALIDATION_ERROR, data)


class PermissionException(ApiException):
    """权限异常"""

    def __init__(self, message: str = "权限不足"):
        super().__init__(message, ErrorCode.PERMISSION_DENIED)


class BusinessException(ApiException):
    """业务异常"""

    def __init__(self, message: str, code: int = ErrorCode.OPERATION_FAILED, data=None):
        super().__init__(message, code, data)


def custom_exception_handler(exc, context):
    """自定义异常处理器"""

    # 处理自定义异常
    if isinstance(exc, ApiException):
        response = ApiResponse.error(message=exc.message, code=exc.code, data=exc.data)
        return response.to_response()

    # 处理DRF默认异常
    response = exception_handler(exc, context)

    if response is not None:
        # 包装DRF异常响应
        if response.status_code == 400:
            api_response = ApiResponse.bad_request(message="请求参数错误", data=response.data)
        elif response.status_code == 401:
            api_response = ApiResponse.unauthorized()
        elif response.status_code == 403:
            api_response = ApiResponse.forbidden()
        elif response.status_code == 404:
            api_response = ApiResponse.not_found()
        else:
            api_response = ApiResponse.error(
                message="请求失败", code=response.status_code, data=response.data
            )

        return Response(data=api_response.to_dict(), status=response.status_code)

    return response
