from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import base64
import os
import uvicorn

from vision import understand_images
from writer import write_copy

app = FastAPI()

@app.post("/generate")
async def generate(files: list[UploadFile] = File(...)):
    images_base64 = []

    for f in files[:5]:
        content = await f.read()
        images_base64.append(base64.b64encode(content).decode())

    image_description = understand_images(images_base64)
    copy = write_copy(image_description)

    return {
        "image_description": image_description,
        "copy": copy
    }

# 增加这段逻辑，让程序能识别 Railway 分配的端口
if __name__ == "__main__":
    # 从环境变量读取端口，Railway 会自动注入这个 $PORT
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)