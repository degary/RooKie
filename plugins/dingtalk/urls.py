"""
钉钉回调URL配置
"""
from django.urls import path
from .handlers import DingtalkCallbackView

urlpatterns = [
    path('callback/', DingtalkCallbackView.as_view(), name='dingtalk_callback'),
]