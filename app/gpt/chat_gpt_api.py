# 카카오톡으로 챗GPT 만들기
from flask import Flask, jsonify, request, current_app
from openai import OpenAI
from . import gpt_bp


# 채팅 모델 컨텍스트
CHAT_MODEL_CONTEXT = ''
# OpenAI API 클라이언트 설정
client = OpenAI(api_key=current_app.config.get("OPEN_AI_API_KEY"))


# API 엔드포인트
@gpt_bp.route('/', methods=['POST'])
def chat_response():
    # 사용자 요청 데이터 추출
    user_request = request.json.get('userRequest', {})
    callback_url = user_request.get('callbackUrl')
    utterance = user_request.get('utterance', '')
    print(f"user_request: {user_request}")
    print(f"callback_url: {callback_url}")
    print(f"utterance: {utterance}")
    # 시스템 컨텍스트로 메시지 리스트 초기화
    messageList = [{"role": "system", "content": CHAT_MODEL_CONTEXT}]
    # 사용자 메시지를 메시지 리스트에 추가
    dicMessage = {"role": "user", "content": utterance}
    messageList.append(dicMessage)
    # OpenAI 채팅 모델에서 응답 받기
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messageList
    )
    response_message = completion.choices[0].message
    # 응답 페이로드 준비
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{response_message.content}"
                    }
                }
            ]
        }
    }
    return jsonify(response)