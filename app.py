import os
import base64
from fastapi import FastAPI, UploadFile, File
import uvicorn

# 确保这些文件名在 GitHub 中是 vision.py 和 writer.py (没有 .txt)
from vision import understand_images
from writer import write_copy

app = FastAPI()

@app.post("/generate")
async def generate(files: list[UploadFile] = File(...)):
    images_base64 = []

    # 只处理前 5 张图片
    for f in files[:5]:
        content = await f.read()
        images_base64.append(base64.b64encode(content).decode())

    # 调用其他模块的函数
    image_description = understand_images(images_base64)
    copy = write_copy(image_description)

    return {
        "image_description": image_description,
        "copy": copy
    }

# 必须放在文件最后，且格式严格如下
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)