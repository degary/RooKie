"""
URL configuration for Rookie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout

def admin_login_redirect(request):
    # 如果是第三方登录回调，不要重定向
    if 'third_party_callback' in request.META.get('HTTP_REFERER', ''):
        return HttpResponse('Login required', status=401)
    # 其他情况重定向到自定义登录页
    return redirect('/login/')

def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

urlpatterns = [
    path('admin/logout/', admin_logout),
    path('admin/login/', admin_login_redirect),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]
