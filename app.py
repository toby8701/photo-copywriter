from fastapi.responses import HTMLResponse
import os
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File
from vision import understand_images
from writer import write_copy

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>AI 朋友圈助手</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: sans-serif; max-width: 500px; margin: auto; padding: 20px; background: #f5f5f5; }
                .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                button { background: #07c160; color: white; border: none; padding: 10px 20px; border-radius: 5px; width: 100%; cursor: pointer; }
                #result { margin-top: 20px; white-space: pre-wrap; background: #f9f9f9; padding: 10px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>📸 朋友圈文案助手</h2>
                <input type="file" id="fileInput" multiple accept="image/*" style="margin-bottom: 20px;">
                <button onclick="upload()">立即生成文案</button>
                <div id="result">等待上传...</div>
            </div>
            <script>
                async def upload() {
                    const files = document.getElementById('fileInput').files;
                    if (files.length === 0) return alert('请先选择图片');
                    
                    const formData = new FormData();
                    for (let f of files) formData.append('files', f);
                    
                    document.getElementById('result').innerText = 'AI 正在思考中...';
                    
                    const resp = await fetch('/generate', { method: 'POST', body: formData });
                    const data = await resp.json();
                    document.getElementById('result').innerHTML = `<b>【画面感】</b><br>${data.image_description}<br><br><b>【朋友圈文案】</b><br>${data.copy}`;
                }
            </script>
        </body>
    </html>
    """
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