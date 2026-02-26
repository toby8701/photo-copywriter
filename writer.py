import os
import google.generativeai as genai
from prompts import WECHAT_COPY_PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def write_copy(image_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = WECHAT_COPY_PROMPT.format(image_description=image_description)
    response = model.generate_content(prompt)
    return response.text if response.candidates else "未能生成文案"