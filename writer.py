import os
import google.generativeai as genai
from prompts import WECHAT_COPY_PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def write_copy(image_description):
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    prompt = WECHAT_COPY_PROMPT.format(image_description=image_description)
    
    try:
        response = model.generate_content(prompt, request_options={"timeout": 60})
        return response.text if response.candidates else "文案生成失败"
    except Exception as e:
        return f"文案API报错: {str(e)}"