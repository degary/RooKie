#!/usr/bin/env python
"""
初始化权限系统
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rookie.settings.dev')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User, SystemModule

def create_system_modules():
    """创建系统模块"""
    modules = [
        {
            'name': 'user_management',
            'display_name': '用户管理',
            'description': '用户和权限管理功能',
            'icon': 'fas fa-users',
            'url_pattern': '/admin/users/'
        },
        {
            'name': 'system_config',
            'display_name': '系统配置',
            'description': '系统参数和配置管理',
            'icon': 'fas fa-cogs',
            'url_pattern': '/admin/config/'
        },
        {
            'name': 'data_analysis',
            'display_name': '数据分析',
            'description': '数据统计和分析功能',
            'icon': 'fas fa-chart-bar',
            'url_pattern': '/admin/analytics/'
        },
        {
            'name': 'file_management',
            'display_name': '文件管理',
            'description': '文件上传和管理功能',
            'icon': 'fas fa-folder',
            'url_pattern': '/admin/files/'
        },
        {
            'name': 'notification',
            'display_name': '消息通知',
            'description': '系统消息和通知功能',
            'icon': 'fas fa-bell',
            'url_pattern': '/admin/notifications/'
        }
    ]
    
    for module_data in modules:
        module, created = SystemModule.objects.get_or_create(
            name=module_data['name'],
            defaults=module_data
        )
        if created:
            print(f"✅ 创建模块: {module.display_name}")
        else:
            print(f"📋 模块已存在: {module.display_name}")

def create_user_groups():
    """创建用户组并分配权限"""
    
    # 获取SystemModule的ContentType
    content_type = ContentType.objects.get_for_model(SystemModule)
    
    # 定义用户组和权限
    groups_permissions = {
        '管理员': {
            'modules': ['user_management', 'system_config'],
            'permissions': ['view', 'add', 'change', 'delete']
        },
        '数据分析师': {
            'modules': ['data_analysis', 'file_management'],
            'permissions': ['view', 'add', 'change']
        },
        '普通员工': {
            'modules': ['notification', 'file_management'],
            'permissions': ['view']
        }
    }
    
    for group_name, config in groups_permissions.items():
        # 创建用户组
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✅ 创建用户组: {group_name}")
        else:
            print(f"📋 用户组已存在: {group_name}")
        
        # 分配权限
        permissions = []
        for module_name in config['modules']:
            for perm_type in config['permissions']:
                codename = f"{perm_type}_systemmodule"
                try:
                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )
                    permissions.append(permission)
                except Permission.DoesNotExist:
                    print(f"⚠️  权限不存在: {codename}")
        
        group.permissions.set(permissions)
        print(f"🔑 为 {group_name} 分配了 {len(permissions)} 个权限")

def assign_users_to_groups():
    """将用户分配到用户组"""
    try:
        # 获取超级用户
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            managers_group = Group.objects.get(name='管理员')
            admin_user.groups.add(managers_group)
            print(f"👤 将 {admin_user.email} 添加到管理员组")
        
        # 可以添加更多用户分配逻辑
        
    except Exception as e:
        print(f"❌ 分配用户到组时出错: {e}")

def main():
    """主函数"""
    print("🚀 开始初始化权限系统...")
    
    # 1. 创建系统模块
    print("\n📋 创建系统模块...")
    create_system_modules()
    
    # 2. 创建用户组并分配权限
    print("\n👥 创建用户组...")
    create_user_groups()
    
    # 3. 分配用户到组
    print("\n🔗 分配用户到组...")
    assign_users_to_groups()
    
    print("\n✅ 权限系统初始化完成！")
    print("\n📝 后续操作:")
    print("1. 访问 http://127.0.0.1:8000/admin/ 管理权限")
    print("2. 在 '用户管理 > 用户' 中为用户分配组")
    print("3. 在 '权限管理 > 用户组' 中调整权限")

if __name__ == '__main__':
    main()