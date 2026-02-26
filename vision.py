import os
import google.generativeai as genai
from prompts import IMAGE_UNDERSTANDING_PROMPT

# 配置
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def understand_images(image_base64_list):
    # 改用这个最轻量的模型，它是目前最不容易报错的
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    
    if not image_base64_list:
        return "错误：没有接收到图片数据"

    # 只取一张图
    img_data = image_base64_list[0]
    content = [
        IMAGE_UNDERSTANDING_PROMPT,
        {"mime_type": "image/jpeg", "data": img_data}
    ]

    try:
        # 强制设置超时为 20 秒，快速反馈
        response = model.generate_content(content, request_options={"timeout": 20})
        return response.text
    except Exception as e:
        # 【关键】这里会把具体的报错信息返回给网页
        error_msg = str(e)
        print(f"CRITICAL ERROR: {error_msg}")
        return f"API报错详情: {error_msg}"
