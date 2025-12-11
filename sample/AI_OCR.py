from openai import OpenAI
from dotenv import load_dotenv

import base64

load_dotenv()

client = OpenAI()


# 投げられた画像を扱えるようにBase64にエンコードする関数
def encode_image(image_path):
    
    # 画像ファイルを読みこみ、Base64エンコードして返す
    with open (image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
    
# エンコードされた画像をOCRにかける関数
def ocr_image(base64_image):
    
    # 生成AIの役割とルールを記述したocr_description.txtの読み取り
    with open("ocr_description.txt", "r", encoding="utf-8") as ocr_file:
        description_txt = ocr_file.read()
        
    # ユーザからの質問文と出力フォーマットを記述したocr_user.txtの読み取り
    with open("ocr_user.txt", "r", encoding="utf-8") as user_file:
        user_txt = user_file.read()
    
    # role:systemの指定として、description_txtで役割とルールを設定
    messages = [{
        "role": "system",
        "content": [{"type": "input_text", "text": description_txt}]
        }
    ]
    
    # role:userの指定として、user_txtで質問文、出力フォーマットとbase64_imageを設定
    messages.append({"role": "user", "content": [
                    {"type": "input_text", "text": user_txt},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}]})
    
    
    #print("DEBUG:", messages)
    
    # respounse APIでの実装
    response = client.responses.create(
        # モデル指定
        model="gpt-4o-mini",
        # messages指定
        input=messages
    )
    
    return response.output_text
    
while True:

    image_path = input("画像ファイルのパスを入力してください: ").strip('"')

    print("画像ファイルパス:", image_path)

    base64_image = encode_image(image_path)

    print("エンコード結果", base64_image[:100] + "...") # 先頭100文字だけ表示

    ocr_result = ocr_image(base64_image)

    print("OCR結果:", ocr_result)