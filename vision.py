import os
import google.generativeai as genai
from prompts import IMAGE_UNDERSTANDING_PROMPT

# 显式配置
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def understand_images(image_base64_list):
    # 使用 Flash-8B，这是目前成功率最高的轻量模型
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    
    if not image_base64_list:
        return "错误：未接收到图片"

    # 测试阶段：强制只处理第一张图，减少数据量
    img_data = image_base64_list[0]
    
    # 构造最标准的请求格式
    content = [
        {"mime_type": "image/jpeg", "data": img_data},
        IMAGE_UNDERSTANDING_PROMPT
    ]

    try:
        # 强制增加 transport='rest' 协议，避开 gRPC 可能被封锁的问题
        # 即使 504 也要让它快速返回具体错误
        response = model.generate_content(
            content,
            request_options={"timeout": 60}
        )
        return response.text if response.candidates else "AI返回空结果"
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG LOG - 详细报错: {error_msg}")
        # 如果是位置不支持，这里会直接写出来
        if "location" in error_msg.lower():
            return "抱歉，当前服务器所在的地区（Railway机房）被Google API限制，请尝试更换API Key所在的区域设置或联系开发者。"
        return f"生成失败原因: {error_msg}"