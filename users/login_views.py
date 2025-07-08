"""
登录页面视图
"""
from django.shortcuts import render
from django.views.generic import TemplateView


class LoginView(TemplateView):
    """自定义登录页面"""
    template_name = 'auth/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Rookie 登录',
            'site_name': 'Rookie 管理平台'
        })
        return context