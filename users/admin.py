from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, ThirdPartyAuthConfig, SystemModule, ModulePermission
from .forms import ThirdPartyAuthConfigForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    
    list_display = ('email', 'username', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'username', 'phone')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('个人信息', {'fields': ('username', 'phone', 'avatar')}),
        ('权限', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理"""
    
    list_display = ('user', 'nickname', 'gender', 'location', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__email', 'nickname', 'location')


@admin.register(ThirdPartyAuthConfig)
class ThirdPartyAuthConfigAdmin(admin.ModelAdmin):
    """第三方认证配置管理"""
    
    form = ThirdPartyAuthConfigForm
    list_display = ('display_name', 'name', 'is_enabled', 'created_at')
    list_filter = ('is_enabled', 'created_at')
    search_fields = ('name', 'display_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'display_name', 'is_enabled')
        }),
        ('配置参数', {
            'fields': ('config',),
            'description': '请按照下方格式填写JSON配置'
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # 为config字段添加帮助文本
        if 'config' in form.base_fields:
            form.base_fields['config'].help_text = self._get_config_help_text(obj)
        
        return form
    
    def _get_config_help_text(self, obj):
        """获取配置帮助文本"""
        return '''
        <div style="margin-top: 10px; font-family: Arial, sans-serif;">
            <h4 style="color: #2c3e50;">🔧 通用配置格式:</h4>
            <pre style="background: #f8f9fa; padding: 12px; border-radius: 6px; border-left: 4px solid #007cba;">{
  "app_id": "应用ID",
  "app_secret": "应用密钥",
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/"
}</pre>
            
            <h4 style="color: #27ae60;">📦 钉钉配置示例 (name: dingtalk):</h4>
            <pre style="background: #e8f5e8; padding: 12px; border-radius: 6px; border-left: 4px solid #27ae60;">{
  "app_id": "dingoa123456789",
  "app_secret": "your_dingtalk_app_secret",
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/",
  "corp_id": "ding123456789"
}</pre>
            <p style="margin: 8px 0; color: #666;"><strong>获取方式:</strong> 钉钉开放平台 > 应用开发 > 创建应用</p>
            
            <h4 style="color: #3498db;">📱 企业微信配置示例 (name: wechat_work):</h4>
            <pre style="background: #e8f4fd; padding: 12px; border-radius: 6px; border-left: 4px solid #3498db;">{
  "app_id": "ww123456789abcdef",
  "app_secret": "your_wechat_work_secret",
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/",
  "corp_id": "ww123456789abcdef"
}</pre>
            <p style="margin: 8px 0; color: #666;"><strong>获取方式:</strong> 企业微信管理后台 > 应用管理 > 创建应用</p>
            
            <h4 style="color: #e74c3c;">⚠️ 注意事项:</h4>
            <ul style="color: #666; line-height: 1.6;">
                <li>请确保 JSON 格式正确，可使用在线 JSON 校验工具</li>
                <li>redirect_uri 必须与第三方平台配置的回调地址一致</li>
                <li>生产环境请修改为实际域名</li>
                <li>保存后请测试登录功能是否正常</li>
            </ul>
        </div>
        '''


@admin.register(SystemModule)
class SystemModuleAdmin(admin.ModelAdmin):
    """系统模块管理"""
    
    list_display = ('display_name', 'name', 'is_active', 'sort_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'display_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'display_name', 'description', 'icon')
        }),
        ('配置信息', {
            'fields': ('url_pattern', 'is_active', 'sort_order')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ModulePermission)
class ModulePermissionAdmin(admin.ModelAdmin):
    """模块权限管理"""
    
    list_display = ('module', 'get_target', 'can_view', 'can_add', 'can_change', 'can_delete', 'granted_at', 'expires_at')
    list_filter = ('module', 'can_view', 'can_add', 'can_change', 'can_delete', 'granted_at')
    search_fields = ('module__display_name', 'user__username', 'user__email', 'group__name')
    readonly_fields = ('granted_by', 'granted_at')
    
    fieldsets = (
        ('权限对象', {
            'fields': ('module', 'user', 'group'),
            'description': '用户和用户组只能选择其一'
        }),
        ('权限设置', {
            'fields': ('can_view', 'can_add', 'can_change', 'can_delete')
        }),
        ('时间设置', {
            'fields': ('expires_at',)
        }),
        ('系统信息', {
            'fields': ('granted_by', 'granted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_target(self, obj):
        if obj.user:
            return f'用户: {obj.user.username}'
        elif obj.group:
            return f'组: {obj.group.name}'
        return '-'
    get_target.short_description = '权限对象'
    
    def save_model(self, request, obj, form, change):
        if not change:  # 新增时记录授权人
            obj.granted_by = request.user
        super().save_model(request, obj, form, change)
    
    def clean(self):
        # 验证用户和组只能选择一个
        if not self.user and not self.group:
            raise ValidationError('必须选择用户或用户组')
        if self.user and self.group:
            raise ValidationError('用户和用户组只能选择其一')