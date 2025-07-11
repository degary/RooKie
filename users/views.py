from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.logger import get_logger
from utils.response import ApiResponse
from plugins.manager import plugin_manager
from .models import User, UserProfile, ThirdPartyAuthConfig
from .serializers import (
    UserSerializer, UserRegistrationSerializer, 
    UserLoginSerializer, UserProfileSerializer
)

logger = get_logger()


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    
    queryset = User.objects.active_users()
    serializer_class = UserSerializer
    permission_classes = []
    
    def get_permissions(self):
        logger.info("检查权限",action=self.action)
        """根据动作设置权限"""
        if self.action in ['register', 'login', 'third_party_auth', 'third_party_callback', 'third_party_providers', 'check_login_status']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info("用户注册成功", 
                       userId=str(user.id), 
                       email=user.email,
                       ip=request.META.get('REMOTE_ADDR'))
            return ApiResponse.created(
                data={'user': UserSerializer(user).data},
                message='注册成功'
            ).to_response()
        return ApiResponse.validation_error(
            message='数据验证失败',
            data=serializer.errors
        ).to_response()
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        logger.info(f"Login request: action={self.action}, method={request.method}, path={request.path}")
        from rest_framework.authtoken.models import Token
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # 获取或创建Token
            token, created = Token.objects.get_or_create(user=user)
            
            logger.info("用户登录成功", 
                       userId=str(user.id), 
                       email=user.email,
                       token_created=created,
                       ip=request.META.get('REMOTE_ADDR'))
            
            return ApiResponse.success(
                data={
                    'user': UserSerializer(user).data,
                    'token': token.key
                },
                message='登录成功'
            ).to_response()
        return ApiResponse.validation_error(
            message='登录信息验证失败',
            data=serializer.errors
        ).to_response()
    
    @action(detail=False, methods=['get'])
    def third_party_providers(self, request):
        """获取可用的第三方登录提供商"""
        configs = ThirdPartyAuthConfig.objects.filter(is_enabled=True)
        providers = []
        
        for config in configs:
            plugin = plugin_manager.get_plugin(config.name, config.config)
            if plugin:
                provider_info = {
                    'name': config.name,
                    'display_name': config.display_name
                }
                
                # 钉钉使用JS SDK，不需要auth_url
                if config.name == 'dingtalk':
                    provider_info['corp_id'] = config.config.get('corp_id', '')
                    provider_info['client_id'] = config.config.get('client_id', '')
                else:
                    # 其他第三方登录需要auth_url
                    provider_info['auth_url'] = plugin.get_auth_url()
                    provider_info['qr_code_url'] = plugin.get_qr_code_url()
                
                providers.append(provider_info)
        
        return ApiResponse.success(
            data={'providers': providers},
            message='获取登录方式成功'
        ).to_response()
    
    @action(detail=False, methods=['get'])
    def third_party_auth(self, request):
        """第三方登录跳转"""
        provider = request.GET.get('provider')
        if not provider:
            return ApiResponse.bad_request('缺少provider参数').to_response()
        
        try:
            config = ThirdPartyAuthConfig.objects.get(name=provider, is_enabled=True)
            plugin = plugin_manager.get_plugin(config.name, config.config)
            
            if not plugin:
                return ApiResponse.error('插件不可用').to_response()
            
            auth_url = plugin.get_auth_url()
            return redirect(auth_url)
            
        except ThirdPartyAuthConfig.DoesNotExist:
            return ApiResponse.not_found('认证提供商不存在').to_response()
    
    @action(detail=False, methods=['get'])
    def third_party_callback(self, request):
        """第三方登录回调"""
        state = request.GET.get('state', '')
        code = request.GET.get('code')
        
        # 从state参数中提取provider
        if state == 'dingtalk_login':
            provider = 'dingtalk'
        elif state == 'wechat_work_login':
            provider = 'wechat_work'
        else:
            provider = state.replace('_login', '') if '_login' in state else state
        
        if not provider or not code:
            return ApiResponse.bad_request('参数错误').to_response()
        
        try:
            config = ThirdPartyAuthConfig.objects.get(name=provider, is_enabled=True)
            plugin = plugin_manager.get_plugin(config.name, config.config)
            
            if not plugin:
                return ApiResponse.error('插件不可用').to_response()
            
            # 获取用户信息
            logger.info(f"开始获取第三方用户信息: {provider}")
            user_info = plugin.get_user_info(code)
            if not user_info:
                logger.error(f"获取第三方用户信息失败: {provider}")
                return ApiResponse.error('获取用户信息失败').to_response()
            
            logger.info(f"成功获取第三方用户信息: {provider}", userinfo=user_info)
            
            # 查找或创建用户
            user = self._get_or_create_user(user_info)
            if not user:
                return ApiResponse.error('用户创建失败').to_response()
            
            # 登录用户到Django session
            login(request, user)
            
            # 检查登录状态
            logger.info(f"登录后状态检查: user={user.email}, is_authenticated={request.user.is_authenticated}, session_key={request.session.session_key}")
            
            if request.user.is_authenticated:
                logger.info(f"第三方登录成功: {provider}, 用户: {user.email}")
                # 返回JSON响应，让前端处理跳转
                return ApiResponse.success(
                    data={'redirect_url': '/admin/'},
                    message='登录成功'
                ).to_response()
            else:
                logger.error(f"第三方登录失败: 用户未正确登录到session")
                return ApiResponse.error('登录失败').to_response()
            
        except Exception as e:
            logger.error("第三方登录失败", provider=provider, error=str(e))
            return ApiResponse.internal_error('登录失败').to_response()
    
    @action(detail=False, methods=['post'])
    def sync_users(self, request):
        """同步第三方用户（仅管理员可用）"""
        # 使用项目权限系统检查权限
        from utils.auth.permissions import permission_checker
        
        if not permission_checker.has_module_permission(request.user, 'user_management', 'change'):
            return ApiResponse.forbidden('您没有用户管理模块的修改权限').to_response()
        
        provider = request.data.get('provider')
        if not provider:
            return ApiResponse.bad_request('缺少provider参数').to_response()
        
        try:
            config = ThirdPartyAuthConfig.objects.get(name=provider, is_enabled=True)
            plugin = plugin_manager.get_plugin(config.name, config.config)
            
            if not plugin:
                return ApiResponse.error('插件不可用').to_response()
            
            synced_count = plugin.sync_users()
            
            logger.info(f"管理员 {request.user.email} 执行用户同步完成", provider=provider, count=synced_count)
            
            return ApiResponse.success(
                data={'count': synced_count},
                message=f'同步完成，共同步 {synced_count} 个用户'
            ).to_response()
            
        except Exception as e:
            logger.error("用户同步失败", provider=provider, error=str(e))
            return ApiResponse.internal_error('同步失败').to_response()
    
    def _get_or_create_user(self, user_info):
        """获取或创建用户"""
        try:
            # 先通过external_id查找
            if user_info.get('external_id'):
                try:
                    return User.objects.get(
                        external_id=user_info['external_id'],
                        auth_source=user_info['source']
                    )
                except User.DoesNotExist:
                    pass
            
            # 通过邮箱查找
            if user_info.get('email'):
                try:
                    user = User.objects.get(email=user_info['email'])
                    # 更新第三方信息
                    user.external_id = user_info.get('external_id')
                    user.auth_source = user_info['source']
                    user.save()
                    return user
                except User.DoesNotExist:
                    pass
            
            # 创建新用户（组织内用户自动注册）
            external_id = user_info.get('external_id') or f"dingtalk_user_{int(__import__('time').time())}"
            username = user_info.get('username') or external_id
            email = user_info.get('email') or f"{external_id}@{user_info['source']}.local"
            
            user_data = {
                'email': email,
                'username': username,
                'phone': user_info.get('phone') or '',
                'avatar': user_info.get('avatar') or '',
                'external_id': external_id,
                'auth_source': user_info['source'],
                'department': user_info.get('department') or '',
                'job_title': user_info.get('job_title') or '',
                'employee_id': user_info.get('employee_id') or '',
                'is_verified': True,
                'is_active': True,  # 组织内用户默认激活
                'is_staff': True
            }
            
            return User.objects.create_user(**user_data)
            
        except Exception as e:
            logger.error(f"创建用户失败: {str(e)}")
            return None
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """用户登出"""
        if request.user.is_authenticated:
            logger.info("用户登出", 
                       userId=str(request.user.id),
                       email=request.user.email)
            logout(request)
        return ApiResponse.success(message='登出成功').to_response()
    

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """获取当前用户信息"""
        return ApiResponse.success(
            data={'user': UserSerializer(request.user).data},
            message='获取用户信息成功'
        ).to_response()
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """更新用户资料"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("用户资料更新", 
                       userId=str(request.user.id),
                       fields=list(request.data.keys()))
            return ApiResponse.success(
                data={'profile': serializer.data},
                message='用户资料更新成功'
            ).to_response()
        return ApiResponse.validation_error(
            message='数据验证失败',
            data=serializer.errors
        ).to_response()
    
    @action(detail=False, methods=['get'])
    def get_token(self, request):
        """获取当前用户Token"""
        from rest_framework.authtoken.models import Token
        
        try:
            token = Token.objects.get(user=request.user)
            return ApiResponse.success(
                data={
                    'token': token.key,
                    'created_at': token.created
                },
                message='Token获取成功'
            ).to_response()
        except Token.DoesNotExist:
            return ApiResponse.not_found('Token不存在').to_response()
    
    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """刷新Token"""
        from rest_framework.authtoken.models import Token
        
        # 删除旧Token，创建新Token
        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)
        
        logger.info("Token刷新成功", userId=str(request.user.id))
        
        return ApiResponse.success(
            data={'token': token.key},
            message='Token刷新成功'
        ).to_response()
    
    @action(detail=False, methods=['delete'])
    def revoke_token(self, request):
        """撤销Token"""
        from rest_framework.authtoken.models import Token
        
        deleted_count = Token.objects.filter(user=request.user).delete()[0]
        
        logger.info("Token撤销成功", userId=str(request.user.id))
        
        return ApiResponse.success(
            data={'deleted_count': deleted_count},
            message='Token已撤销'
        ).to_response()
    
    @action(detail=False, methods=['get'])
    def my_modules(self, request):
        """获取当前用户可访问的模块"""
        from utils.auth.permissions import permission_checker
        
        modules = permission_checker.get_user_modules(request.user)
        module_data = []
        
        for module in modules:
            module_data.append({
                'name': module.name,
                'display_name': module.display_name,
                'description': module.description,
                'icon': module.icon,
                'url_pattern': module.url_pattern,
                'permissions': {
                    'can_view': permission_checker.has_module_permission(request.user, module.name, 'view'),
                    'can_add': permission_checker.has_module_permission(request.user, module.name, 'add'),
                    'can_change': permission_checker.has_module_permission(request.user, module.name, 'change'),
                    'can_delete': permission_checker.has_module_permission(request.user, module.name, 'delete'),
                }
            })
        
        return ApiResponse.success(
            data={
                'modules': module_data,
                'user_info': {
                    'username': request.user.username,
                    'email': request.user.email,
                    'department': request.user.department,
                    'job_title': request.user.job_title,
                    'is_superuser': request.user.is_superuser
                }
            },
            message='获取用户模块权限成功'
        ).to_response()
    
    @action(detail=False, methods=['get'])
    def check_login_status(self, request):
        """检查登录状态（用于二维码登录轮询）"""
        # 这里可以根据实际需要实现更复杂的逻辑
        # 比如检查session或者缓存中的登录状态
        is_logged_in = request.user.is_authenticated
        
        return ApiResponse.success(
            data={'logged_in': is_logged_in},
            message='状态检查成功'
        ).to_response()