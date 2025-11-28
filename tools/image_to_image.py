from collections.abc import Generator
from typing import Any

import requests
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class ImageToImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 获取凭据（支持两种模式：自定义 API 与 OpenAI 兼容 API）
        api_url = self.runtime.credentials.get("api_url")
        api_key = self.runtime.credentials.get("api_key")
        openai_base_url = self.runtime.credentials.get("openai_base_url")
        openai_api_key = self.runtime.credentials.get("openai_api_key")
        openai_organization_id = self.runtime.credentials.get("openai_organization_id")
        
        # 获取输入参数
        model = tool_parameters.get("model") or self.runtime.credentials.get("image_model")
        prompt = tool_parameters.get("prompt")
        negative_prompt = tool_parameters.get("negative_prompt", "")
        image_url = tool_parameters.get("image_url")
        width = tool_parameters.get("width", 512)
        height = tool_parameters.get("height", 512)
        steps = tool_parameters.get("steps", 20)
        cfg_scale = tool_parameters.get("cfg_scale", 7.5)
        seed = tool_parameters.get("seed")
        n = tool_parameters.get("n", 1)
        
        # 验证参数
        self._validate_parameters(image_url, width, height, steps, cfg_scale, n)
        
        # 调用第三方API生成图像
        result = self._call_third_party_api(
            api_url=api_url,
            api_key=api_key,
            model=model,
            task_type="image-to-image",
            prompt=prompt,
            negative_prompt=negative_prompt,
            image_url=image_url,
            width=width,
            height=height,
            steps=steps,
            cfg_scale=cfg_scale,
            seed=seed,
            n=n,
            openai_base_url=openai_base_url,
            openai_api_key=openai_api_key,
            openai_organization_id=openai_organization_id,
        )
        
        # 返回结果
        yield self.create_json_message(result)
    
    def _validate_parameters(self, image_url, width, height, steps, cfg_scale, n):
        """
        验证输入参数
        """
        # 验证图生图参数
        if not image_url:
            raise Exception("图生图任务必须提供image_url参数")
        
        # 验证图像尺寸
        if width < 64 or width > 4096:
            raise Exception(f"图像宽度必须在64-4096之间，当前值：{width}")
        if height < 64 or height > 4096:
            raise Exception(f"图像高度必须在64-4096之间，当前值：{height}")
        
        # 验证生成步数
        if steps < 1 or steps > 100:
            raise Exception(f"生成步数必须在1-100之间，当前值：{steps}")
        
        # 验证提示词引导强度
        if cfg_scale < 0 or cfg_scale > 30:
            raise Exception(f"提示词引导强度必须在0-30之间，当前值：{cfg_scale}")
        
        # 验证生成图像数量
        if n < 1 or n > 10:
            raise Exception(f"生成图像数量必须在1-10之间，当前值：{n}")
    
    def _call_third_party_api(self, api_url, api_key, model, task_type, prompt, negative_prompt, image_url, width, height, steps, cfg_scale, seed, n, openai_base_url, openai_api_key, openai_organization_id):
        """
        调用第三方AI平台API生成图像
        """
        base = (api_url or "").rstrip("/")
        if base.endswith("/v1"):
            request_url = f"{base}/image/edits"
        elif base.endswith("/image/edits") or base.endswith("/images/edits"):
            request_url = base
        else:
            request_url = api_url
        payload = {
            "model": model,
            "prompt": prompt,
            "image_url": image_url,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if width and height:
            payload["image_size"] = f"{width}x{height}"
        if steps is not None:
            payload["num_inference_steps"] = steps
        if cfg_scale is not None:
            payload["guidance_scale"] = cfg_scale
        if seed is not None:
            payload["seed"] = seed
        if n is not None:
            payload["batch_size"] = n
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        
        try:
            # 发送请求
            response = requests.post(request_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()  # 抛出HTTP错误
            
            # 解析响应
            result = response.json()
            
            # 验证响应格式
            if not isinstance(result, dict):
                raise ValueError("第三方API返回格式错误，响应不是JSON对象")
            
            image_url_out = None
            response_seed = result.get("seed", seed)
            if isinstance(result.get("images"), list) and result["images"]:
                first = result["images"][0]
                image_url_out = first.get("url") or first.get("image_url")
            elif isinstance(result.get("data"), list) and result["data"]:
                first = result["data"][0]
                image_url_out = first.get("url") or first.get("image_url")
            elif isinstance(result.get("image_url"), str):
                image_url_out = result.get("image_url")
            if not image_url_out:
                raise ValueError("第三方API返回中缺少图片链接字段")
            
            # 返回结果并同时输出图片消息
            yield self.create_json_message({
                "image_url": image_url_out,
                "seed": response_seed
            })
            yield self.create_image_message(image_url=image_url_out)
        except requests.exceptions.RequestException as e:
            # 处理网络请求异常
            if hasattr(e, 'response') and e.response is not None:
                raise Exception(f"调用第三方API失败：{e.response.status_code} {e.response.reason} - {e.response.text[:200]}...")
            else:
                raise Exception(f"调用第三方API失败：{str(e)}")
        except json.JSONDecodeError:
            # 处理JSON解析异常
            raise Exception("第三方API返回格式错误，无法解析JSON")
        except Exception as e:
            # 处理其他异常
            raise Exception(f"生成图像失败：{str(e)}")
