"""
响应中间件
"""
from django.http import JsonResponse

from .wrapper import ApiResponse


class ResponseMiddleware:
    """响应格式化中间件"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 只处理API请求
        if request.path.startswith("/api/"):
            # 如果是JsonResponse且不是标准格式，进行包装
            if isinstance(response, JsonResponse):
                try:
                    data = response.json()
                    # 检查是否已经是标准格式
                    if not all(key in data for key in ["success", "code", "message"]):
                        # 包装为标准格式
                        api_response = ApiResponse.success(data=data)
                        return JsonResponse(api_response.to_dict())
                except:
                    pass

        return response
