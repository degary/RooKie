"""
API响应包装器
"""
import uuid
from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status


class ErrorCode:
    """错误码定义"""
    # 成功
    SUCCESS = 200
    CREATED = 201
    
    # 客户端错误
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    VALIDATION_ERROR = 422
    
    # 服务器错误
    INTERNAL_ERROR = 500
    
    # 业务错误
    USER_NOT_EXIST = 1001
    PERMISSION_DENIED = 1002
    INVALID_PARAMS = 1003
    OPERATION_FAILED = 1004


class ApiResponse:
    """API响应包装器"""
    
    def __init__(self, success: bool, code: int, message: str, data=None, request_id: str = None):
        self.success = success
        self.code = code
        self.message = message
        self.data = data
        self.timestamp = timezone.now().isoformat()
        self.request_id = request_id or str(uuid.uuid4())[:8]
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            'success': self.success,
            'code': self.code,
            'message': self.message,
            'timestamp': self.timestamp,
            'request_id': self.request_id
        }
        
        if self.data is not None:
            result['data'] = self.data
            
        return result
    
    def to_response(self) -> Response:
        """转换为DRF Response对象"""
        return Response(
            data=self.to_dict(),
            status=self.code if self.code < 600 else 200
        )
    
    @classmethod
    def success(cls, data=None, message: str = "操作成功", code: int = ErrorCode.SUCCESS):
        """成功响应"""
        return cls(success=True, code=code, message=message, data=data)
    
    @classmethod
    def created(cls, data=None, message: str = "创建成功"):
        """创建成功响应"""
        return cls(success=True, code=ErrorCode.CREATED, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "操作失败", code: int = ErrorCode.BAD_REQUEST, data=None):
        """错误响应"""
        return cls(success=False, code=code, message=message, data=data)
    
    @classmethod
    def bad_request(cls, message: str = "请求参数错误", data=None):
        """请求参数错误"""
        return cls(success=False, code=ErrorCode.BAD_REQUEST, message=message, data=data)
    
    @classmethod
    def unauthorized(cls, message: str = "未授权访问"):
        """未授权"""
        return cls(success=False, code=ErrorCode.UNAUTHORIZED, message=message)
    
    @classmethod
    def forbidden(cls, message: str = "权限不足"):
        """权限不足"""
        return cls(success=False, code=ErrorCode.FORBIDDEN, message=message)
    
    @classmethod
    def not_found(cls, message: str = "资源不存在"):
        """资源不存在"""
        return cls(success=False, code=ErrorCode.NOT_FOUND, message=message)
    
    @classmethod
    def validation_error(cls, message: str = "数据验证失败", data=None):
        """数据验证错误"""
        return cls(success=False, code=ErrorCode.VALIDATION_ERROR, message=message, data=data)
    
    @classmethod
    def internal_error(cls, message: str = "服务器内部错误"):
        """服务器内部错误"""
        return cls(success=False, code=ErrorCode.INTERNAL_ERROR, message=message)
    
    @classmethod
    def business_error(cls, message: str, code: int = ErrorCode.OPERATION_FAILED, data=None):
        """业务错误"""
        return cls(success=False, code=code, message=message, data=data)
    
    def __str__(self):
        return f"ApiResponse(success={self.success}, code={self.code}, message='{self.message}')"
    
    def __repr__(self):
        return self.__str__()