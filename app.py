import os
import base64
from fastapi import FastAPI, UploadFile, File
import uvicorn

# 确认这些是你的文件名（确保 GitHub 上没有 .txt 后缀）
from vision import understand_images
from writer import write_copy

app = FastAPI()

@app.post("/generate")
async def generate(files: list[UploadFile] = File(...)):
    images_base64 = []

    # 处理上传的文件
    for f in files[:5]:
        content = await f.read()
        images_base64.append(base64.b64encode(content).decode())

    # 调用图片理解和文案生成函数
    image_description = understand_images(images_base64)
    copy = write_copy(image_description)

    return {
        "image_description": image_description,
        "copy": copy
    }

# Railway 启动逻辑
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)