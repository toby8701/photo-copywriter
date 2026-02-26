import openai
from prompts import IMAGE_UNDERSTANDING_PROMPT

openai.api_key = "YOUR_API_KEY"

def understand_images(image_files):
    messages = [
        {"role": "system", "content": IMAGE_UNDERSTANDING_PROMPT}
    ]

    for img in image_files:
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image_url": f"data:image/jpeg;base64,{img}"
                }
            ]
        )

    resp = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.4
    )

    return resp.choices[0].message.content