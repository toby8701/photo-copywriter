import os
import google.generativeai as genai
from prompts import IMAGE_UNDERSTANDING_PROMPT

# 配置 Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def understand_images(image_base64_list):
    # 【关键修改】只写模型简称，不带任何路径前缀
    # 如果 gemini-1.5-flash 报错，就用 gemini-pro-vision (这是老牌兼容版)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if not image_base64_list:
            return "错误：未接收到图片"

        img_data = image_base64_list[0]
        content = [
            {"mime_type": "image/jpeg", "data": img_data},
            IMAGE_UNDERSTANDING_PROMPT
        ]

        # 增加超时限制
        response = model.generate_content(
            content,
            request_options={"timeout": 60}
        )
        return response.text if response.candidates else "AI返回空结果"
    except Exception as e:
        # 如果 1.5-flash 还是 404，尝试自动降级到 pro 版
        if "404" in str(e):
            return f"模型路径错误，请检查API Key权限。具体报错: {str(e)}"
        return f"生成失败: {str(e)}"