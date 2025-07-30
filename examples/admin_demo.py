"""
Admin后台演示脚本
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# 设置Django环境
env = os.environ.get("DJANGO_ENV", "dev")
settings_module = "Rookie.settings." + env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)


import django

django.setup()

from django.contrib.auth.models import Group, Permission

from users.models import User, UserProfile


def create_demo_data():
    """创建演示数据"""

    print("🚀 创建演示数据...")

    # 创建用户组
    admin_group, _ = Group.objects.get_or_create(name="管理员")
    user_group, _ = Group.objects.get_or_create(name="普通用户")

    # 创建测试用户
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "is_staff": True,
            "is_superuser": True,
            "is_verified": True,
        },
        {
            "email": "user1@example.com",
            "username": "user1",
            "phone": "13800138001",
            "is_verified": True,
        },
        {
            "email": "user2@example.com",
            "username": "user2",
            "phone": "13800138002",
            "is_verified": False,
        },
    ]

    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data["email"], defaults=user_data
        )
        if created:
            user.set_password("password123")
            user.save()

            # 创建用户资料
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "nickname": f"{user.username}的昵称",
                    "bio": f"这是{user.username}的个人简介",
                    "gender": "male" if user.username != "user2" else "female",
                    "location": "北京市",
                },
            )

            print(f"✅ 创建用户: {user.email}")

    print(f"\n🎉 演示数据创建完成!")
    print(f"📊 用户总数: {User.objects.count()}")
    print(f"📋 用户资料: {UserProfile.objects.count()}")

    print(f"\n🔑 登录信息:")
    print(f"   超级用户: admin@example.com / password123")
    print(f"   普通用户: user1@example.com / password123")
    print(f"   未验证用户: user2@example.com / password123")

    print(f"\n🌐 访问后台: http://127.0.0.1:8000/admin/")


if __name__ == "__main__":
    create_demo_data()
