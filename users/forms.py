"""
用户相关表单
"""
from django import forms
from django.core.exceptions import ValidationError
import json
from .models import ThirdPartyAuthConfig


class ThirdPartyAuthConfigForm(forms.ModelForm):
    """第三方认证配置表单"""
    
    class Meta:
        model = ThirdPartyAuthConfig
        fields = '__all__'
        widgets = {
            'config': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80,
                'placeholder': '''请输入JSON格式的配置，例如：
{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret", 
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/"
}'''
            })
        }
    
    def clean_config(self):
        """验证config字段的JSON格式"""
        config_data = self.cleaned_data.get('config')
        
        if not config_data:
            raise ValidationError('配置信息不能为空')
        
        # 验证JSON格式
        try:
            if isinstance(config_data, str):
                config_dict = json.loads(config_data)
            else:
                config_dict = config_data
        except json.JSONDecodeError as e:
            raise ValidationError(f'JSON格式错误: {str(e)}')
        
        # 验证必需字段
        required_fields = ['app_id', 'app_secret', 'redirect_uri']
        missing_fields = [field for field in required_fields if not config_dict.get(field)]
        
        if missing_fields:
            raise ValidationError(f'缺少必需字段: {", ".join(missing_fields)}')
        
        # 验证redirect_uri格式
        redirect_uri = config_dict.get('redirect_uri', '')
        if not redirect_uri.startswith(('http://', 'https://')):
            raise ValidationError('redirect_uri必须是有效的URL地址')
        
        return config_dict
    
    def clean_name(self):
        """验证插件名称"""
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError('插件名称不能为空')
        
        # 验证插件名称格式
        allowed_names = ['dingtalk', 'wechat_work', 'feishu', 'github', 'google']
        if name not in allowed_names:
            raise ValidationError(f'不支持的插件名称，支持的插件: {", ".join(allowed_names)}')
        
        return name