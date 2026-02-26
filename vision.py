import os
import dashscope
from dashscope import MultiModalConversation
from prompts import IMAGE_UNDERSTANDING_PROMPT

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

def understand_images(image_base64_list):
    # 构造通义千问要求的格式
    messages = [{
        'role': 'user',
        'content': [{'text': IMAGE_UNDERSTANDING_PROMPT}]
    }]
    
    # 阿里要求 base64 必须带上头
    for img_b64 in image_base64_list[:3]: # 先取3张防止超时
        messages[0]['content'].append({
            'image': f'data:image/jpeg;base64,{img_b64}'
        })

    try:
        responses = MultiModalConversation.call(
            model='qwen-vl-max', # 阿里最强的视觉模型
            messages=messages
        )
        if responses.status_code == 200:
            return responses.output.choices[0].message.content[0]['text']
        else:
            return f"阿里API报错: {responses.message}"
    except Exception as e:
        return f"系统错误: {str(e)}"