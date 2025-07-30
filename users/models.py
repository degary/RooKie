import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractUser):
    """自定义用户模型"""

    # 使用UUID作为主键
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 基本信息
    email = models.EmailField("邮箱", unique=True)
    phone = models.CharField("手机号", max_length=20, blank=True, null=True)
    avatar = models.URLField("头像", blank=True, null=True)

    # 状态字段
    is_verified = models.BooleanField("已验证", default=False)
    is_deleted = models.BooleanField("已删除", default=False)

    # 第三方登录字段
    external_id = models.CharField(
        "外部ID",
        max_length=100,
        blank=True,
        null=True,
        help_text="对于 dingtalk，此字段对应unionId",
    )
    auth_source = models.CharField("认证来源", max_length=50, blank=True, null=True)
    dingtalk_user_id = models.CharField("钉钉用户ID", max_length=100, blank=True, null=True)

    # 组织信息
    department = models.CharField("部门", max_length=100, blank=True, null=True)
    departments = models.ManyToManyField("Department", blank=True, verbose_name="所属部门")
    job_title = models.CharField("职位", max_length=100, blank=True, null=True)
    employee_id = models.CharField("工号", max_length=50, blank=True, null=True)

    # 时间字段
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    last_login_ip = models.GenericIPAddressField("最后登录IP", blank=True, null=True)

    # 使用email作为登录字段
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # 自定义管理器
    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class Department(models.Model):
    """部门模型"""

    name = models.CharField(max_length=100, verbose_name="部门名称")
    external_id = models.CharField(max_length=100, verbose_name="外部ID")
    parent_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="父部门ID"
    )
    source = models.CharField(max_length=50, verbose_name="来源系统")
    order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "users_department"
        verbose_name = "部门"
        verbose_name_plural = "部门"
        unique_together = ["external_id", "source"]

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """用户扩展信息"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField("昵称", max_length=50, blank=True)
    bio = models.TextField("个人简介", blank=True)
    birthday = models.DateField("生日", blank=True, null=True)
    gender = models.CharField(
        "性别",
        max_length=10,
        choices=[("male", "男"), ("female", "女"), ("other", "其他")],
        blank=True,
    )
    location = models.CharField("所在地", max_length=100, blank=True)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"


class ThirdPartyAuthConfig(models.Model):
    """第三方认证配置"""

    name = models.CharField("插件名称", max_length=50, unique=True)
    display_name = models.CharField("显示名称", max_length=100)
    is_enabled = models.BooleanField("是否启用", default=False)
    config = models.JSONField("配置信息", default=dict)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "third_party_auth_configs"
        verbose_name = "第三方认证配置"
        verbose_name_plural = "第三方认证配置"

    def __str__(self):
        return self.display_name


class SystemModule(models.Model):
    """系统模块"""

    name = models.CharField("模块名称", max_length=50, unique=True)
    display_name = models.CharField("显示名称", max_length=100)
    description = models.TextField("模块描述", blank=True)
    icon = models.CharField("图标", max_length=50, blank=True)
    url_pattern = models.CharField("URL模式", max_length=200, blank=True)
    is_active = models.BooleanField("是否启用", default=True)
    sort_order = models.IntegerField("排序", default=0)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "system_modules"
        verbose_name = "系统模块"
        verbose_name_plural = "系统模块"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.display_name


class ModulePermission(models.Model):
    """模块权限配置"""

    module = models.ForeignKey(
        SystemModule, on_delete=models.CASCADE, related_name="permissions"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(
        "auth.Group", on_delete=models.CASCADE, blank=True, null=True
    )

    # 权限类型
    can_view = models.BooleanField("可查看", default=False)
    can_add = models.BooleanField("可新增", default=False)
    can_change = models.BooleanField("可修改", default=False)
    can_delete = models.BooleanField("可删除", default=False)

    granted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="granted_permissions"
    )
    granted_at = models.DateTimeField("授权时间", auto_now_add=True)
    expires_at = models.DateTimeField("过期时间", blank=True, null=True)

    class Meta:
        db_table = "module_permissions"
        verbose_name = "模块权限"
        verbose_name_plural = "模块权限"
        unique_together = [["module", "user"], ["module", "group"]]

    def __str__(self):
        target = self.user.username if self.user else self.group.name
        return f"{self.module.display_name} - {target}"

    @property
    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at
