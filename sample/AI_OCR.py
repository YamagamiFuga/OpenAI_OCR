from openai import OpenAI
from dotenv import load_dotenv

import base64

load_dotenv()

client = OpenAI()

#image_path = "C:\Users\fuga1\OneDrive\画像\meter2.jpg"

def encode_image(image_path):
    with open (image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
    

def ocr_image(base64_image):
    with open("ocr_description.txt", "r", encoding="utf-8") as ocr_file:
        description_txt = ocr_file.read()
        
    with open("ocr_user.txt", "r", encoding="utf-8") as user_file:
        user_txt = user_file.read()
        
    messages = [{
        "role": "system",
        "content": [{"type": "input_text", "text": description_txt}]
        }
    ]
    
    messages.append({"role": "user", "content": [
                    {"type": "input_text", "text": user_txt},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}]})
    
    
    #print("DEBUG:", messages)
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages
    )
    
    return response.output_text
    

image_path = input("画像ファイルのパスを入力してください: ").strip('"')

print("画像ファイルパス:", image_path)

base64_image = encode_image(image_path)

print("エンコード結果", base64_image[:100] + "...") # 先頭100文字だけ表示

ocr_result = ocr_image(base64_image)

print("OCR結果:", ocr_result)