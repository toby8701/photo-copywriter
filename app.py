import os
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from vision import understand_images
from writer import write_copy

app = FastAPI(title="朋友圈文案大师")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>朋友圈文案助手</title>
        <style>
            :root { --primary-color: #07c160; }
            body { font-family: -apple-system, system-ui, sans-serif; background: #f0f2f5; margin: 0; display: flex; justify-content: center; padding: 20px; }
            .container { background: white; width: 100%; max-width: 450px; border-radius: 16px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
            h2 { text-align: center; color: #333; margin-bottom: 8px; }
            p.hint { text-align: center; color: #888; font-size: 14px; margin-bottom: 24px; }
            
            /* 缩略图样式 */
            #preview-container { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px; justify-content: center; }
            .preview-img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid #eee; }

            .upload-area { border: 2px dashed #ddd; border-radius: 12px; padding: 30px 20px; text-align: center; cursor: pointer; transition: 0.3s; }
            .upload-area:hover { border-color: var(--primary-color); background: #f7fff9; }
            #fileInput { display: none; }
            
            .btn { background: var(--primary-color); color: white; border: none; padding: 14px; border-radius: 10px; width: 100%; font-size: 16px; font-weight: bold; margin-top: 20px; cursor: pointer; }
            .btn:disabled { background: #ccc; cursor: not-allowed; }
            
            #result-box { margin-top: 24px; display: none; border-top: 1px solid #eee; padding-top: 20px; }
            .label { font-size: 12px; color: var(--primary-color); font-weight: bold; margin-bottom: 8px; display: block; }
            .content { background: #f9f9f9; padding: 15px; border-radius: 8px; font-size: 15px; line-height: 1.6; color: #333; margin-bottom: 16px; white-space: pre-wrap; position: relative; }
            .copy-btn { font-size: 12px; color: var(--primary-color); cursor: pointer; float: right; text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📸 朋友圈助手</h2>
            <p class="hint">上传照片，即刻获取生活记录</p>
            
            <div id="preview-container"></div>

            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <span id="upload-text">点击选择照片 (建议1-3张)</span>
                <input type="file" id="fileInput" multiple accept="image/*" onchange="updateFiles()">
            </div>

            <button id="submitBtn" class="btn" onclick="generate()">开始生成文案</button>

            <div id="result-box">
                <span class="label">为您生成的文案 <span class="copy-btn" onclick="copyText()">一键复制全部</span></span>
                <div id="copy-content" class="content"></div>
            </div>
        </div>

        <script>
            // 更新图片预览
            function updateFiles() {
                const input = document.getElementById('fileInput');
                const container = document.getElementById('preview-container');
                container.innerHTML = ''; 
                
                const files = input.files;
                if(files.length > 0) {
                    document.getElementById('upload-text').innerText = `已选 ${files.length} 张照片，点击可重选`;
                }

                for (const file of files) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.className = 'preview-img';
                        container.appendChild(img);
                    }
                    reader.readAsDataURL(file);
                }
            }

            // 调用后端生成
            async function generate() {
                const files = document.getElementById('fileInput').files;
                if (files.length === 0) return alert('请先选择照片');
                
                const btn = document.getElementById('submitBtn');
                const resultBox = document.getElementById('result-box');
                const copyContent = document.getElementById('copy-content');
                
                btn.disabled = true;
                btn.innerText = 'AI 正在感受画面...';
                resultBox.style.display = 'none';

                const formData = new FormData();
                for (let f of files) formData.append('files', f);

                try {
                    const resp = await fetch('/generate', { method: 'POST', body: formData });
                    const data = await resp.json();
                    
                    if (data.copy) {
                        copyContent.innerText = data.copy;
                        resultBox.style.display = 'block';
                    } else {
                        throw new Error("生成失败");
                    }
                } catch (e) {
                    alert('生成失败，可能是网络波动，请重试');
                } finally {
                    btn.disabled = false;
                    btn.innerText = '重新生成';
                }
            }

            // 复制功能
            function copyText() {
                const text = document.getElementById('copy-content').innerText;
                navigator.clipboard.writeText(text).then(() => alert('文案已复制'));
            }
        </script>
    </body>
    </html>
    """

@app.post("/generate")
async def generate_api(files: list[UploadFile] = File(...)):
    images_base64 = []
    # 阿里接口建议不要传太多大图，这里限制前3张
    for f in files[:3]:
        content = await f.read()
        images_base64.append(base64.b64encode(content).decode())
    
    # 1. 识别氛围 (调用 vision.py)
    desc = understand_images(images_base64)
    
    # 2. 写文案 (调用 writer.py)
    copy_text = write_copy(desc)
    
    # 3. 只返回文案给前端展示
    return {"copy": copy_text}

if __name__ == "__main__":
    # 保持你之前运行成功的 8080 端口
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)