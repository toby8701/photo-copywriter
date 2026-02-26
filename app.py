import os
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File
from vision import understand_images
from writer import write_copy

app = FastAPI()

@app.post("/generate")
async def generate(files: list[UploadFile] = File(...)):
    images_base64 = []
    for f in files[:5]:
        content = await f.read()
        images_base64.append(base64.b64encode(content).decode())
    
    desc = understand_images(images_base64)
    copy_text = write_copy(desc)
    
    return {"image_description": desc, "copy": copy_text}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)