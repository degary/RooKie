"""
初始化系统模块和权限
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rookie.settings.dev')

import django
django.setup()

from users.models import SystemModule, ModulePermission
from django.contrib.auth.models import Group


def create_system_modules():
    """创建系统模块"""
    modules = [
        {
            'name': 'user_management',
            'display_name': '👥 用户管理',
            'description': '用户账户管理、权限分配',
            'icon': 'fas fa-users',
            'url_pattern': '/admin/users/',
            'sort_order': 1
        },
        {
            'name': 'system_config',
            'display_name': '⚙️ 系统配置',
            'description': '系统参数配置、第三方集成',
            'icon': 'fas fa-cogs',
            'url_pattern': '/admin/config/',
            'sort_order': 2
        },
        {
            'name': 'data_analysis',
            'display_name': '📊 数据分析',
            'description': '业务数据统计分析',
            'icon': 'fas fa-chart-bar',
            'url_pattern': '/analytics/',
            'sort_order': 3
        },
        {
            'name': 'file_management',
            'display_name': '📁 文件管理',
            'description': '文件上传下载管理',
            'icon': 'fas fa-folder',
            'url_pattern': '/files/',
            'sort_order': 4
        },
        {
            'name': 'notification',
            'display_name': '🔔 消息通知',
            'description': '系统消息推送管理',
            'icon': 'fas fa-bell',
            'url_pattern': '/notifications/',
            'sort_order': 5
        }
    ]
    
    created_count = 0
    for module_data in modules:
        module, created = SystemModule.objects.get_or_create(
            name=module_data['name'],
            defaults=module_data
        )
        if created:
            created_count += 1
            print(f"✅ 创建模块: {module.display_name}")
        else:
            print(f"ℹ️  模块已存在: {module.display_name}")
    
    print(f"\n📋 共创建 {created_count} 个新模块")
    return SystemModule.objects.all()


def create_default_groups():
    """创建默认用户组"""
    groups_data = [
        {
            'name': 'managers',
            'display_name': '管理员',
            'permissions': ['user_management', 'system_config'],
            'permission_types': ['view', 'add', 'change', 'delete']
        },
        {
            'name': 'analysts',
            'display_name': '数据分析师',
            'permissions': ['data_analysis', 'file_management'],
            'permission_types': ['view', 'add']
        },
        {
            'name': 'employees',
            'display_name': '普通员工',
            'permissions': ['notification', 'file_management'],
            'permission_types': ['view']
        }
    ]
    
    created_count = 0
    for group_data in groups_data:
        group, created = Group.objects.get_or_create(
            name=group_data['name']
        )
        if created:
            created_count += 1
            print(f"✅ 创建用户组: {group_data['display_name']}")
        else:
            print(f"ℹ️  用户组已存在: {group_data['display_name']}")
        
        # 分配权限
        for module_name in group_data['permissions']:
            try:
                module = SystemModule.objects.get(name=module_name)
                permission, perm_created = ModulePermission.objects.get_or_create(
                    module=module,
                    group=group,
                    defaults={
                        'can_view': 'view' in group_data['permission_types'],
                        'can_add': 'add' in group_data['permission_types'],
                        'can_change': 'change' in group_data['permission_types'],
                        'can_delete': 'delete' in group_data['permission_types'],
                    }
                )
                if perm_created:
                    print(f"  └─ 分配权限: {module.display_name}")
            except SystemModule.DoesNotExist:
                print(f"  ⚠️  模块不存在: {module_name}")
    
    print(f"\n👥 共创建 {created_count} 个新用户组")
    return Group.objects.all()


def main():
    """主函数"""
    print("🚀 初始化系统模块和权限...")
    
    # 创建系统模块
    print("\n1️⃣ 创建系统模块:")
    modules = create_system_modules()
    
    # 创建默认用户组和权限
    print("\n2️⃣ 创建用户组和权限:")
    groups = create_default_groups()
    
    print("\n✅ 初始化完成！")
    print("\n📋 使用说明:")
    print("1. 在Admin后台 -> 用户管理 -> 用户 中将用户添加到对应用户组")
    print("2. 或者在 模块权限 中为特定用户分配权限")
    print("3. 用户登录后调用 /api/users/my_modules/ 查看可访问的模块")
    
    print(f"\n📊 统计信息:")
    print(f"- 系统模块: {modules.count()} 个")
    print(f"- 用户组: {groups.count()} 个")
    print(f"- 权限配置: {ModulePermission.objects.count()} 条")


if __name__ == "__main__":
    main()