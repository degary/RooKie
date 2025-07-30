# DRF Spectacular API文档系统使用指南

## 概述

DRF Spectacular 是一个为 Django REST Framework 自动生成 OpenAPI 3.0 规范文档的工具，提供了现代化的 API 文档界面。

## 功能特性

- 🚀 **自动生成**: 基于代码自动生成 OpenAPI 3.0 文档
- 📱 **现代界面**: 提供 Swagger UI 和 ReDoc 两种文档界面
- 🔧 **高度可配置**: 支持丰富的配置选项
- 🎯 **类型安全**: 完整的类型提示和验证
- 🔍 **在线测试**: 支持在文档界面直接测试 API

## 访问地址

| 功能 | 地址 | 说明 |
|------|------|------|
| Swagger UI | `/api/docs/` | 交互式 API 文档界面 |
| ReDoc | `/api/redoc/` | 美观的文档阅读界面 |
| OpenAPI Schema | `/api/schema/` | 原始 JSON/YAML 格式 |

## 配置说明

### 基础配置

```python
# settings.py
SPECTACULAR_SETTINGS = {
    'TITLE': 'Rookie API',                    # API 标题
    'DESCRIPTION': '企业级Django Web应用API文档',  # API 描述
    'VERSION': '1.0.0',                       # API 版本
    'SERVE_INCLUDE_SCHEMA': False,            # 是否在文档中包含 schema
    'COMPONENT_SPLIT_REQUEST': True,          # 分离请求和响应组件
    'SCHEMA_PATH_PREFIX': '/api/',            # API 路径前缀
}
```

### 高级配置选项

```python
SPECTACULAR_SETTINGS = {
    # 认证配置
    'SECURITY': [
        {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'Token',
        }
    ],

    # 服务器配置
    'SERVERS': [
        {'url': 'http://127.0.0.1:8000', 'description': '开发环境'},
        {'url': 'https://api.example.com', 'description': '生产环境'},
    ],

    # 标签配置
    'TAGS': [
        {'name': 'users', 'description': '用户管理'},
        {'name': 'auth', 'description': '认证授权'},
    ],

    # 自定义扩展
    'EXTENSIONS_INFO': {
        'x-logo': {
            'url': 'https://example.com/logo.png',
            'altText': 'Logo'
        }
    }
}
```

## ViewSet 文档化

### 基础文档化

```python
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(summary="获取用户列表", tags=["users"]),
    create=extend_schema(summary="创建用户", tags=["users"]),
    retrieve=extend_schema(summary="获取用户详情", tags=["users"]),
    update=extend_schema(summary="更新用户", tags=["users"]),
    destroy=extend_schema(summary="删除用户", tags=["users"]),
)
class UserViewSet(viewsets.ModelViewSet):
    """用户管理 ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### Action 文档化

```python
@extend_schema(
    summary="用户登录",
    description="通过邮箱和密码进行用户登录",
    request=UserLoginSerializer,
    responses={
        200: UserSerializer,
        400: "请求参数错误",
        401: "认证失败"
    },
    tags=["auth"]
)
@action(detail=False, methods=['post'])
def login(self, request):
    """用户登录"""
    pass
```

## Serializer 文档化

### 字段文档化

```python
from drf_spectacular.utils import extend_schema_field

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        help_text="用户密码，至少8位字符"
    )

    @extend_schema_field(serializers.CharField)
    def get_full_name(self, obj):
        """获取用户全名"""
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {
            'email': {'help_text': '用户邮箱地址'},
            'username': {'help_text': '用户名，唯一标识'},
        }
```

### 示例数据

```python
from drf_spectacular.utils import OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'Valid Login',
            summary='正确的登录请求',
            description='使用有效的邮箱和密码进行登录',
            value={
                'email': 'user@example.com',
                'password': 'password123'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Login Success',
            summary='登录成功响应',
            value={
                'success': True,
                'data': {
                    'user': {'id': 1, 'email': 'user@example.com'},
                    'token': 'abc123...'
                }
            },
            response_only=True,
        ),
    ]
)
@action(detail=False, methods=['post'])
def login(self, request):
    pass
```

## 自定义响应格式

### 统一响应格式

```python
from drf_spectacular.utils import OpenApiResponse

# 定义通用响应 Serializer
class ApiResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False)

@extend_schema(
    responses={
        200: OpenApiResponse(
            response=ApiResponseSerializer,
            description="成功响应"
        ),
        400: OpenApiResponse(
            response=ApiResponseSerializer,
            description="请求错误"
        ),
    }
)
def my_view(request):
    pass
```

## 认证文档化

### Token 认证

```python
from drf_spectacular.utils import OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='Authorization',
            type=str,
            location=OpenApiParameter.HEADER,
            description='Token认证头，格式: Token <your_token>',
            required=True
        ),
    ]
)
def protected_view(request):
    pass
```

## 过滤和分页文档化

### 查询参数

```python
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            type=str,
            description='搜索关键词',
            required=False
        ),
        OpenApiParameter(
            name='ordering',
            type=str,
            description='排序字段',
            required=False
        ),
    ]
)
@action(detail=False, methods=['get'])
def search(self, request):
    pass
```

## 最佳实践

### 1. 统一的文档风格

```python
# 为所有 ViewSet 使用统一的标签和描述格式
@extend_schema_view(
    list=extend_schema(summary="获取列表", tags=["模块名"]),
    create=extend_schema(summary="创建记录", tags=["模块名"]),
    # ...
)
```

### 2. 详细的错误响应

```python
@extend_schema(
    responses={
        200: UserSerializer,
        400: OpenApiResponse(description="请求参数验证失败"),
        401: OpenApiResponse(description="未授权访问"),
        403: OpenApiResponse(description="权限不足"),
        404: OpenApiResponse(description="资源不存在"),
        500: OpenApiResponse(description="服务器内部错误"),
    }
)
```

### 3. 版本管理

```python
# 为不同版本的 API 使用不同的配置
SPECTACULAR_SETTINGS = {
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api/v1/',
}
```

## 常见问题

### Q: 如何隐藏某些 API？

```python
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)
def internal_api(request):
    pass
```

### Q: 如何自定义 Schema？

```python
from drf_spectacular.openapi import AutoSchema

class CustomAutoSchema(AutoSchema):
    def get_operation_id(self):
        return f"{self.method.lower()}_{self.path.replace('/', '_')}"

# 在 ViewSet 中使用
class MyViewSet(viewsets.ModelViewSet):
    schema = CustomAutoSchema()
```

### Q: 如何处理文件上传？

```python
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary'
                }
            }
        }
    }
)
def upload_file(request):
    pass
```

## 部署注意事项

### 生产环境配置

```python
# 生产环境建议禁用文档
if not DEBUG:
    SPECTACULAR_SETTINGS['SERVE_INCLUDE_SCHEMA'] = False
    # 或者完全移除文档 URL
```

### 性能优化

```python
SPECTACULAR_SETTINGS = {
    'DISABLE_ERRORS_AND_WARNINGS': True,  # 禁用警告
    'ENUM_NAME_OVERRIDES': {              # 枚举名称覆盖
        'ValidationErrorEnum': 'django.core.exceptions.ValidationError',
    },
}
```

## 总结

DRF Spectacular 提供了强大的 API 文档自动生成功能，通过合理的配置和文档化，可以大大提升 API 的可维护性和开发效率。建议在项目开发过程中持续完善 API 文档，确保文档与代码保持同步。
