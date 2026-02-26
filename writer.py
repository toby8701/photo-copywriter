import os
import google.generativeai as genai
from prompts import WECHAT_COPY_PROMPT

# 从 Railway 环境变量中读取 Gemini 密钥
# 请确保你在 Railway Variables 中添加了名为 GEMINI_API_KEY 的变量
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def write_copy(image_description):
    # 初始化模型（推荐使用 1.5-flash，速度快且免费额度高）
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 填充你的微信文案 Prompt 
    prompt = WECHAT_COPY_PROMPT.format(
        image_description=image_description
    )

    # 生成内容
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
        )
    )

    return response.text