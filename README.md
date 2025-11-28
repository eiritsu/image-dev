# 第三方AI图像生成插件

A Dify plugin for generating images through third-party AI platform URLs and APIs.

## 功能特性

### Features

- ✅ 支持文生图（text-to-image）
- ✅ 支持图生图（image-to-image）
- ✅ 兼容OpenAI API格式
- ✅ 支持自定义API URL和API密钥
- ✅ 支持多种参数配置：
  - 图像宽度和高度
  - 生成步数
  - 提示词引导强度
  - 随机种子
  - 负面提示词
  - 生成图像数量
- ✅ 支持Bearer Token认证

## 快速开始

### Quick Start

1. 将插件目录打包为zip文件
2. 登录Dify平台
3. 进入「插件中心」
4. 点击「上传插件」
5. 选择打包好的zip文件上传
6. 等待插件审核通过

## 配置与使用

### Configuration & Usage

### 1. 配置插件

#### 1. Configure Plugin

在使用插件前，需要配置以下参数：

Before using the plugin, you need to configure the following parameters:

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| api_url | string | 是 | https://api.openai.com | 第三方AI平台的API URL，兼容OpenAI API格式 |
| api_key | string | 是 | - | 第三方AI平台的API密钥 |
| model | string | 否 | dall-e-3 | 使用的图像生成模型，如dall-e-3、dall-e-2等 |

### 2. 文生图使用

#### 2. Text-to-Image Usage

1. 选择「文生图」任务类型
2. 输入提示词（prompt）
3. 可选：输入负面提示词（negative_prompt）
4. 可选：调整图像宽度、高度、生成步数、引导强度、随机种子、生成数量
5. 点击「生成」

### 3. 图生图使用

#### 3. Image-to-Image Usage

1. 选择「图生图」任务类型
2. 输入提示词（prompt）
3. 输入原始图像URL（image_url）
4. 可选：输入负面提示词（negative_prompt）
5. 可选：调整图像宽度、高度、生成步数、引导强度、随机种子、生成数量
6. 点击「生成」

## API 要求

### API Requirements

### 请求格式

#### Request Format

第三方API需要支持POST请求，请求体格式如下：

The third-party API must support POST requests with the following request body format:

```json
{
  "task_type": "text-to-image" or "image-to-image",
  "prompt": "生成图像的提示词",
  "negative_prompt": "负面提示词",
  "width": 512,
  "height": 512,
  "steps": 20,
  "cfg_scale": 7.5,
  "seed": 12345,  // 可选
  "image_url": "原始图像URL"  // 仅图生图任务需要
}
```

### 响应格式

#### Response Format

第三方API需要返回以下格式的JSON响应：

The third-party API must return a JSON response in the following format:

```json
{
  "image_url": "生成的图像URL",
  "seed": 12345  // 可选，实际使用的随机种子
}
```

### 认证方式

#### Authentication Method

第三方API需要支持Bearer Token认证，在请求头中添加：

The third-party API must support Bearer Token authentication, added in the request header:

```
Authorization: Bearer {api_key}
```

## 技术规格

### Technical Specifications

- **运行环境**: Python 3.12
- **依赖**: 
  - dify_plugin>=0.4.0,<0.7.0
  - requests>=2.28.0
- **超时时间**: 120秒
- **支持架构**: amd64, arm64

## 注意事项

### Notes

1. 请确保第三方API的URL和API密钥正确
2. 请确保第三方API支持文生图和图生图功能
3. 请确保第三方API的响应格式符合要求
4. 生成的图像URL需要是可公开访问的
5. 插件会设置120秒的请求超时，请确保第三方API能够在120秒内返回结果

## 故障排除

### Troubleshooting

### 常见错误

#### Common Errors

1. **API调用失败**：请检查API URL和API密钥是否正确
2. **返回格式错误**：请检查第三方API的响应格式是否符合要求
3. **图生图失败**：请确保提供了有效的image_url
4. **超时错误**：请检查第三方API的响应时间是否超过120秒

### 调试建议

#### Debugging Suggestions

1. 使用Postman等工具测试第三方API是否正常工作
2. 检查第三方API的文档，确保请求格式正确
3. 查看Dify平台的日志，获取详细的错误信息

## 项目结构

### Project Structure

```
├── _assets/              # 插件图标资源
├── provider/             # 图像生成服务提供者
├── tools/                # 工具定义
│   ├── image_generator.py      # 图像生成主逻辑
│   ├── image_to_image.py       # 图生图工具
│   └── text_to_image.py        # 文生图工具
├── .env                  # 环境变量配置
├── .env.example          # 环境变量示例
├── main.py               # 插件入口
├── manifest.yaml         # 插件清单
├── plugin.json           # 插件配置
└── requirements.txt      # 依赖列表
```

## 版本历史

### Version History

- v1.0.0：初始版本，支持文生图和图生图功能

## 许可证

### License

MIT License

## 贡献

### Contribution

欢迎提交Issue和Pull Request！

Contributions are welcome! Feel free to submit Issues and Pull Requests.

### Contact

- 项目地址：https://github.com/eiritsu/image-dev
- 作者：eiritsu
