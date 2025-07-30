"""
第三方认证配置示例
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rookie.settings.dev")

import django

django.setup()

from users.models import ThirdPartyAuthConfig


def setup_dingtalk_config():
    """配置钉钉登录"""
    config, created = ThirdPartyAuthConfig.objects.get_or_create(
        name="dingtalk",
        defaults={
            "display_name": "钉钉登录",
            "is_enabled": True,
            "config": {
                "app_id": "your_dingtalk_app_id",  # 钉钉应用的AppId
                "app_secret": "your_dingtalk_app_secret",  # 钉钉应用的AppSecret
                "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/",  # 回调地址
                "corp_id": "your_corp_id",  # 企业ID（可选，用于企业内部应用）
            },
        },
    )

    if created:
        print("✅ 钉钉配置创建成功")
    else:
        print("ℹ️  钉钉配置已存在")

    return config


def setup_wechat_work_config():
    """配置企业微信登录"""
    config, created = ThirdPartyAuthConfig.objects.get_or_create(
        name="wechat_work",
        defaults={
            "display_name": "企业微信登录",
            "is_enabled": True,
            "config": {
                "app_id": "your_wechat_work_app_id",  # 企业微信应用ID
                "app_secret": "your_wechat_work_secret",  # 企业微信应用Secret
                "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/",
                "corp_id": "your_corp_id",  # 企业ID
            },
        },
    )

    if created:
        print("✅ 企业微信配置创建成功")
    else:
        print("ℹ️  企业微信配置已存在")

    return config


def main():
    """创建第三方认证配置"""
    print("🔧 设置第三方认证配置...")

    # 创建钉钉配置
    dingtalk_config = setup_dingtalk_config()

    # 创建企业微信配置
    wechat_config = setup_wechat_work_config()

    print("\n📋 配置完成！")
    print("请在Admin后台修改以下配置：")
    print("1. 访问 http://127.0.0.1:8000/admin/users/thirdpartyauthconfig/")
    print("2. 编辑对应的配置项")
    print("3. 填入真实的app_id、app_secret等参数")

    print("\n🔑 需要配置的参数：")
    print("钉钉:")
    print("  - app_id: 钉钉开放平台应用的AppId")
    print("  - app_secret: 钉钉开放平台应用的AppSecret")
    print("  - redirect_uri: 授权回调地址")

    print("\n企业微信:")
    print("  - app_id: 企业微信应用ID")
    print("  - app_secret: 企业微信应用Secret")
    print("  - corp_id: 企业微信企业ID")
    print("  - redirect_uri: 授权回调地址")


if __name__ == "__main__":
    main()
