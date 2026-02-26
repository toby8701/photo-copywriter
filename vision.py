import os
import google.generativeai as genai
from prompts import IMAGE_UNDERSTANDING_PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def understand_images(image_base64_list):
    # 换回最稳的模型名字
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if not image_base64_list:
        return "错误：未接收到图片"

    img_data = image_base64_list[0]
    content = [
        {"mime_type": "image/jpeg", "data": img_data},
        IMAGE_UNDERSTANDING_PROMPT
    ]

    try:
        # 增加 transport='rest' 强行走网页协议，避开端口封锁
        response = model.generate_content(
            content,
            request_options={"timeout": 60}
        )
        return response.text if response.candidates else "AI返回空结果"
    except Exception as e:
        return f"生成失败原因: {str(e)}"