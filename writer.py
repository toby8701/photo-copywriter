import os
import dashscope
from dashscope import Generation
from prompts import WECHAT_COPY_PROMPT

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

def write_copy(image_description):
    prompt = WECHAT_COPY_PROMPT.format(image_description=image_description)
    try:
        response = Generation.call(
            model='qwen-plus',
            prompt=prompt
        )
        if response.status_code == 200:
            return response.output.text
        else:
            return f"文案生成报错: {response.message}"
    except Exception as e:
        return f"系统错误: {str(e)}"