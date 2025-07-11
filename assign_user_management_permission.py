#!/usr/bin/env python
"""
为用户分配用户管理权限的脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rookie.settings.dev')
django.setup()

from users.models import User, SystemModule, ModulePermission

# 获取用户管理模块
try:
    module = SystemModule.objects.get(name='user_management')
except SystemModule.DoesNotExist:
    print("❌ 请先创建 user_management 模块")
    exit(1)

# 为超级用户分配权限（示例）
admin_email = input("请输入要授权的用户邮箱: ")

try:
    user = User.objects.get(email=admin_email)
    
    # 创建或更新权限
    permission, created = ModulePermission.objects.get_or_create(
        module=module,
        user=user,
        defaults={
            'can_view': True,
            'can_add': True,
            'can_change': True,
            'can_delete': True
        }
    )
    
    if created:
        print(f"✅ 成功为用户 {user.email} 分配用户管理权限")
    else:
        print(f"ℹ️ 用户 {user.email} 已有用户管理权限")
        
except User.DoesNotExist:
    print(f"❌ 用户 {admin_email} 不存在")