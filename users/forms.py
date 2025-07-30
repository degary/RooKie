"""
用户相关表单
"""
import json

from django import forms
from django.core.exceptions import ValidationError

from .models import ThirdPartyAuthConfig


class ThirdPartyAuthConfigForm(forms.ModelForm):
    """第三方认证配置表单"""

    class Meta:
        model = ThirdPartyAuthConfig
        fields = "__all__"
        widgets = {
            "config": forms.Textarea(
                attrs={
                    "rows": 12,
                    "cols": 80,
                    "placeholder": """请输入JSON格式的配置，不同平台字段不同：

钉钉 (dingtalk):
{
  "client_id": "dingoa987654321",
  "client_secret": "your_client_secret",
  "app_id": "dingoa123456789",
  "corp_id": "ding123456789abcdef",
  "redirect_uri": "https://your-domain.com/api/users/third_party_callback/"
}

企业微信 (wechat_work):
{
  "corp_id": "ww123456789abcdef",
  "agent_id": "1000001",
  "secret": "your_wechat_work_secret",
  "redirect_uri": "https://your-domain.com/api/users/third_party_callback/"
}""",
                }
            )
        }

    def clean_config(self):
        """验证config字段的JSON格式"""
        config_data = self.cleaned_data.get("config")
        name = self.cleaned_data.get("name", "")

        if not config_data:
            raise ValidationError("配置信息不能为空")

        # 验证JSON格式
        try:
            if isinstance(config_data, str):
                config_dict = json.loads(config_data)
            else:
                config_dict = config_data
        except json.JSONDecodeError as e:
            raise ValidationError(f"JSON格式错误: {str(e)}")

        # 根据不同平台验证必需字段
        validation_result = self._validate_platform_config(name, config_dict)
        if validation_result:
            raise ValidationError(validation_result)

        # 验证redirect_uri格式
        redirect_uri = config_dict.get("redirect_uri", "")
        if redirect_uri and not redirect_uri.startswith(("http://", "https://")):
            raise ValidationError("redirect_uri必须是有效的URL地址")

        return config_dict

    def _validate_platform_config(self, platform_name, config_dict):
        """验证不同平台的配置字段"""
        platform_requirements = {
            "dingtalk": {
                "required": ["client_id", "client_secret", "redirect_uri"],
                "optional": ["app_id", "agent_id", "corp_id"],
            },
            "wechat_work": {
                "required": ["corp_id", "agent_id", "secret", "redirect_uri"],
                "optional": [],
            },
            "feishu": {
                "required": ["app_id", "app_secret", "redirect_uri"],
                "optional": [],
            },
            "github": {
                "required": ["client_id", "client_secret", "redirect_uri"],
                "optional": [],
            },
            "google": {
                "required": ["client_id", "client_secret", "redirect_uri"],
                "optional": [],
            },
        }

        if platform_name not in platform_requirements:
            return f"不支持的平台: {platform_name}"

        requirements = platform_requirements[platform_name]
        required_fields = requirements["required"]

        # 检查必需字段
        missing_fields = [
            field for field in required_fields if not config_dict.get(field)
        ]

        if missing_fields:
            return f'{platform_name}平台缺少必需字段: {", ".join(missing_fields)}'

        return None

    def clean_name(self):
        """验证插件名称"""
        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError("插件名称不能为空")

        # 验证插件名称格式
        allowed_names = ["dingtalk", "wechat_work", "feishu", "github", "google"]
        if name not in allowed_names:
            raise ValidationError(f'不支持的插件名称，支持的插件: {", ".join(allowed_names)}')

        return name
