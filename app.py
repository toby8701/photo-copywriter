import os
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File

# 确保 vision.py 和 writer.py 在仓库根目录且没有 .txt 后缀
from vision import understand_images
from writer import write_copy

app = FastAPI()

@app.post("/generate")
async def generate(files: list[UploadFile] = File(...)):
    images_base64 = []
    for f in files[:5]:
        content = await f.read()
        images_base64.append(base64.b64encode(content).decode())
    
    # 1. 获取图片理解
    desc = understand_images(images_base64)
    # 2. 生成文案
    copy_text = write_copy(desc)
    
    # 3. 返回结果（请务必确保这里是大括号结束）
    return {"image_description": desc, "copy": copy_text}

if __name__ == "__main__":
    # 获取 Railway 自动分配的端口
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)