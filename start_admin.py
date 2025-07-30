#!/usr/bin/env python
"""
快速启动Admin后台的脚本
"""
import os
import subprocess
import sys


def main():
    """启动Admin后台"""

    print("🚀 启动 Rookie Admin 后台...")

    # 安装依赖
    print("📦 检查依赖...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
        )
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return

    # 设置环境
    os.environ.setdefault("DJANGO_ENV", "dev")

    # 创建迁移
    print("🔄 创建数据库迁移...")
    try:
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ 数据库迁移完成")
    except subprocess.CalledProcessError:
        print("❌ 数据库迁移失败")
        return

    # 创建演示数据
    print("📊 创建演示数据...")
    try:
        subprocess.run([sys.executable, "examples/admin_demo.py"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  演示数据创建失败，但不影响使用")

    # 启动服务器
    print("🌐 启动开发服务器...")
    print("📱 Admin后台地址: http://127.0.0.1:8000/admin/")
    print("🔑 登录账号: admin@example.com / password123")
    print("⏹️  按 Ctrl+C 停止服务器")

    try:
        subprocess.run([sys.executable, "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")


if __name__ == "__main__":
    main()
