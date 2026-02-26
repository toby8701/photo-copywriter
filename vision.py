import os
import google.generativeai as genai
from prompts import IMAGE_UNDERSTANDING_PROMPT

# 配置 API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def understand_images(image_base64_list):
    # 使用支持多模态的 Gemini 1.5 Flash 模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 构建内容列表：提示词 + 所有图片数据
    content = [IMAGE_UNDERSTANDING_PROMPT]
    
    for img_data in image_base64_list:
        content.append({
            "mime_type": "image/jpeg",
            "data": img_data
        })

    # 发送给 Gemini 进行识别
    response = model.generate_content(content)
    
    if response.candidates:
        return response.text
    else:
        return "图片识别失败，请检查图片格式。"