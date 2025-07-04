from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """自定义用户管理器"""
    
    def create_user(self, email, password=None, **extra_fields):
        """创建普通用户"""
        if not email:
            raise ValueError('邮箱不能为空')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)
    
    def active_users(self):
        """获取活跃用户"""
        return self.filter(is_active=True, is_deleted=False)
    
    def verified_users(self):
        """获取已验证用户"""
        return self.active_users().filter(is_verified=True)