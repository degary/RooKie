# API响应包装器使用指南

## 📋 概述

API响应包装器提供统一的响应格式，支持API接口和普通函数调用，确保所有返回值格式一致。

## 🎯 标准响应格式

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {...},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "abc12345"
}
```

## 🚀 快速开始

### 1. 导入模块

```python
from utils.response import ApiResponse, ApiException, api_response
```

### 2. API视图中使用

#### 基本用法

```python
from rest_framework.decorators import api_view
from utils.response import ApiResponse

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return ApiResponse.success(
            data={'user': UserSerializer(user).data},
            message="获取用户信息成功"
        ).to_response()
    except User.DoesNotExist:
        return ApiResponse.not_found("用户不存在").to_response()
```

#### 使用装饰器

```python
from utils.response import api_response

@api_response
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    return {'users': UserSerializer(users, many=True).data}
    # 自动包装为标准格式
```

### 3. ViewSet中使用

```python
from rest_framework import viewsets
from utils.response import ApiResponse

class UserViewSet(viewsets.ModelViewSet):

    def list(self, request):
        users = User.objects.all()
        return ApiResponse.success(
            data={'users': UserSerializer(users, many=True).data},
            message="获取用户列表成功"
        ).to_response()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return ApiResponse.created(
                data={'user': UserSerializer(user).data},
                message="用户创建成功"
            ).to_response()
        else:
            return ApiResponse.validation_error(
                message="数据验证失败",
                data=serializer.errors
            ).to_response()
```

### 4. 普通函数中使用

```python
from utils.response import ApiResponse, function_response

# 手动包装
def create_user_profile(user_data):
    try:
        user = User.objects.create(**user_data)
        return ApiResponse.success(
            data={'user_id': user.id},
            message="用户创建成功"
        )
    except Exception as e:
        return ApiResponse.error(f"创建失败: {str(e)}")

# 使用装饰器
@function_response
def get_user_stats():
    return {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count()
    }
```

## 📚 API参考

### ApiResponse 类方法

#### 成功响应

```python
# 基本成功响应
ApiResponse.success(data=None, message="操作成功", code=200)

# 创建成功响应
ApiResponse.created(data=None, message="创建成功")
```

#### 错误响应

```python
# 通用错误
ApiResponse.error(message="操作失败", code=400, data=None)

# 请求参数错误
ApiResponse.bad_request(message="请求参数错误", data=None)

# 未授权
ApiResponse.unauthorized(message="未授权访问")

# 权限不足
ApiResponse.forbidden(message="权限不足")

# 资源不存在
ApiResponse.not_found(message="资源不存在")

# 数据验证错误
ApiResponse.validation_error(message="数据验证失败", data=None)

# 服务器内部错误
ApiResponse.internal_error(message="服务器内部错误")

# 业务错误
ApiResponse.business_error(message="业务处理失败", code=1004, data=None)
```

### 错误码定义

```python
class ErrorCode:
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
```

## 🔧 高级用法

### 1. 自定义异常

```python
from utils.response import ApiException, BusinessException

# 抛出业务异常
def transfer_money(from_user, to_user, amount):
    if from_user.balance < amount:
        raise BusinessException("余额不足", code=1005)

    # 执行转账逻辑...
    return ApiResponse.success(message="转账成功")
```

### 2. 异常处理

```python
from utils.response import ApiException

@api_view(['POST'])
def some_api(request):
    try:
        # 业务逻辑
        result = do_something()
        return ApiResponse.success(data=result).to_response()
    except ApiException as e:
        # 自定义异常会被全局异常处理器自动处理
        raise e
    except Exception as e:
        return ApiResponse.internal_error(f"操作失败: {str(e)}").to_response()
```

### 3. 分页响应

```python
from django.core.paginator import Paginator

def get_users_paginated(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page = paginator.get_page(request.GET.get('page', 1))

    return ApiResponse.success(
        data={
            'users': UserSerializer(page.object_list, many=True).data,
            'pagination': {
                'current_page': page.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page.has_next(),
                'has_previous': page.has_previous()
            }
        }
    ).to_response()
```

### 4. 条件响应

```python
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return ApiResponse.not_found("用户不存在").to_response()

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return ApiResponse.success(
            data={'user': serializer.data},
            message="用户更新成功"
        ).to_response()
    else:
        return ApiResponse.validation_error(
            message="数据验证失败",
            data=serializer.errors
        ).to_response()
```

## 🎨 最佳实践

### 1. 消息规范

```python
# ✅ 好的消息
ApiResponse.success(message="用户创建成功")
ApiResponse.error(message="邮箱格式不正确")

# ❌ 避免的消息
ApiResponse.success(message="ok")
ApiResponse.error(message="error")
```

### 2. 数据结构

```python
# ✅ 结构化数据
ApiResponse.success(data={
    'user': user_data,
    'permissions': permissions_data
})

# ✅ 列表数据
ApiResponse.success(data={
    'users': users_data,
    'total': total_count
})
```

### 3. 错误处理

```python
# ✅ 详细的错误信息
ApiResponse.validation_error(
    message="表单验证失败",
    data={
        'email': ['邮箱格式不正确'],
        'password': ['密码长度至少8位']
    }
)
```

### 4. 业务逻辑分离

```python
# ✅ 业务逻辑在service层
class UserService:
    @staticmethod
    def create_user(user_data):
        # 业务逻辑
        if User.objects.filter(email=user_data['email']).exists():
            return ApiResponse.business_error("邮箱已存在")

        user = User.objects.create(**user_data)
        return ApiResponse.created(data={'user_id': user.id})

# API层只负责调用
@api_view(['POST'])
def create_user_api(request):
    result = UserService.create_user(request.data)
    return result.to_response()
```

## 🔍 调试技巧

### 1. 响应对象检查

```python
response = ApiResponse.success(data={'test': 'data'})
print(response)  # 打印响应信息
print(response.to_dict())  # 查看字典格式
```

### 2. 请求ID追踪

```python
# 每个响应都包含唯一的request_id，便于日志追踪
response = ApiResponse.success(data={'user_id': 123})
print(f"Request ID: {response.request_id}")
```

## ⚠️ 注意事项

1. **不要重复包装**: 如果函数已返回ApiResponse对象，不要再次包装
2. **异常处理**: 使用全局异常处理器，避免在每个视图中重复处理
3. **性能考虑**: 大量数据时注意序列化性能
4. **向后兼容**: 渐进式改造现有API，避免破坏性变更

## 🔗 相关链接

- [Django REST Framework 文档](https://www.django-rest-framework.org/)
- [HTTP状态码参考](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
