import os
import google.generativeai as genai
from prompts import IMAGE_UNDERSTANDING_PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def understand_images(image_base64_list):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # 组合 Prompt 和图片
    content = [IMAGE_UNDERSTANDING_PROMPT]
    for img_data in image_base64_list:
        content.append({"mime_type": "image/jpeg", "data": img_data})
    
    response = model.generate_content(content)
    return response.text if response.candidates else "未能识别图片内容"