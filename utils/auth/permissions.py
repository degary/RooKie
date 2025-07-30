"""
权限检查工具
"""
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from users.models import ModulePermission, SystemModule
from utils.logger import get_logger

logger = get_logger()


class ModulePermissionChecker:
    """模块权限检查器"""

    @staticmethod
    def has_module_permission(user, module_name, permission_type="view"):
        """
        检查用户是否有模块权限

        Args:
            user: 用户对象
            module_name: 模块名称
            permission_type: 权限类型 (view/add/change/delete)

        Returns:
            bool: 是否有权限
        """
        if not user.is_authenticated:
            return False

        # 超级用户拥有所有权限
        if user.is_superuser:
            return True

        try:
            module = SystemModule.objects.get(name=module_name, is_active=True)
        except SystemModule.DoesNotExist:
            logger.warning("模块不存在", module_name=module_name, user_id=user.id)
            return False

        # 检查用户直接权限
        user_permission = ModulePermission.objects.filter(
            module=module, user=user
        ).first()

        if user_permission and not user_permission.is_expired:
            return getattr(user_permission, f"can_{permission_type}", False)

        # 检查用户组权限
        for group in user.groups.all():
            group_permission = ModulePermission.objects.filter(
                module=module, group=group
            ).first()

            if group_permission and not group_permission.is_expired:
                if getattr(group_permission, f"can_{permission_type}", False):
                    return True

        return False

    @staticmethod
    def get_user_modules(user):
        """获取用户可访问的模块列表"""
        if not user.is_authenticated:
            return []

        if user.is_superuser:
            return SystemModule.objects.filter(is_active=True).order_by(
                "sort_order", "name"
            )

        # 获取用户直接权限的模块
        user_modules = set()

        # 用户直接权限
        user_permissions = ModulePermission.objects.filter(
            user=user, can_view=True
        ).select_related("module")

        for perm in user_permissions:
            if not perm.is_expired and perm.module.is_active:
                user_modules.add(perm.module)

        # 用户组权限
        for group in user.groups.all():
            group_permissions = ModulePermission.objects.filter(
                group=group, can_view=True
            ).select_related("module")

            for perm in group_permissions:
                if not perm.is_expired and perm.module.is_active:
                    user_modules.add(perm.module)

        return sorted(user_modules, key=lambda x: (x.sort_order, x.name))


def require_module_permission(module_name, permission_type="view"):
    """
    装饰器：要求模块权限

    Usage:
        @require_module_permission('user_management', 'view')
        def user_list(request):
            pass
    """

    def decorator(view_func):
        def check_permission(user):
            return ModulePermissionChecker.has_module_permission(
                user, module_name, permission_type
            )

        return user_passes_test(check_permission)(view_func)

    return decorator


class ModulePermissionMixin(UserPassesTestMixin):
    """
    类视图权限混入

    Usage:
        class UserListView(ModulePermissionMixin, ListView):
            module_name = 'user_management'
            permission_type = 'view'
    """

    module_name = None
    permission_type = "view"

    def test_func(self):
        if not self.module_name:
            raise ValueError("必须设置 module_name")

        return ModulePermissionChecker.has_module_permission(
            self.request.user, self.module_name, self.permission_type
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        raise PermissionDenied(f"您没有访问 {self.module_name} 模块的权限")


def check_module_permission(request, module_name, permission_type="view"):
    """
    在视图中直接检查权限

    Usage:
        def my_view(request):
            check_module_permission(request, 'user_management', 'view')
            # 继续处理...
    """
    if not ModulePermissionChecker.has_module_permission(
        request.user, module_name, permission_type
    ):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())

        raise PermissionDenied(f"您没有访问 {module_name} 模块的权限")


# 全局权限检查器实例
permission_checker = ModulePermissionChecker()
