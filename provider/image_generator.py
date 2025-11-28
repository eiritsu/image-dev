from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class ImageGeneratorProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            api_url = credentials.get('api_url')
            api_key = credentials.get('api_key')
            image_model = credentials.get('image_model')
            if not api_url:
                raise ValueError('API URL 不能为空')
            if not api_key:
                raise ValueError('API Key 不能为空')
            if not image_model:
                raise ValueError('图像模型名称不能为空')
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
