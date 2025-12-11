from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

#print("AI_API:", os.getenv("OPENAI_API_KEY"))

# 日本語での応答を指示するプロンプト
description_txt = "あなたは優秀なアシスタントです。ユーザーからの質問に対して、正確かつ日本語で簡潔に答えてください。"
    
# 会話履歴を保持するためのメッセージリスト
messages = [
    {"role": "system", "content": description_txt}
]

def question_text(request: str):
    
    # ユーザーからの質問をメッセージリストに追加
    messages.append({"role": "user", "content": request})
    
    
    # OpenAIのAPIを呼び出して応答を取得
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages
    )

    
    # 応答メッセージを会話履歴に追加
    history_message = response.output_text
    
    # 会話履歴にアシスタントの応答を追加
    messages.append({"role": "assistant", "content": history_message})
    
    
    # 応答テキストを返す
    return response.output_text

"""

comlentions版コード

def question_text(request: str):
    
    # ユーザーからの質問をメッセージリストに追加
    messages.append({"role": "user", "content": request})
    
    #print("DEBUG:", messages)
    
    # OpenAIのAPIを呼び出して応答を取得
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    
    # 応答メッセージを会話履歴に追加
    history_message = response.choices[0].message.content
    
    # 会話履歴にアシスタントの応答を追加
    messages.append({"role": "assistant", "content": history_message})
    
    
    
    # 応答テキストを返す
    return response.choices[0].message.content
"""

while True:
    request = input("質問をどうぞ: ")

    res = question_text(request)

    print("AI回答:", res)