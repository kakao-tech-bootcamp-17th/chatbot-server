# 카카오톡으로 챗GPT 만들기
from flask import Flask, jsonify, request, current_app
from openai import OpenAI
from . import gpt_bp
import json


# OpenAI API 클라이언트 설정
# client = OpenAI(api_key=current_app.config.get("OPEN_AI_API_KEY"))
OPENAI_API_KEY = current_app.config.get("OPEN_AI_API_KEY")

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
    return jsonify(response)


'''Abby 코드 추가'''
def call_gpt_api(model, prompt, utterance, max_tokens=2000, temperature=0.2):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": utterance}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response
    except Exception as e:
        print(f"예외처리 되었습니다: {e}")
        return None


def chatAnalyze(utterance) :
    # OpenAI API 키 설정 (Project Key 사용하기)
    OPENAI_API_KEY = OPENAI_API_KEY
    model = "gpt-4o-mini"

    # 프롬프트 설정
    prompt = f"""
    당신은 사용자 발화로부터 지역명을 추출하고, 어떤 정보가 필요한지에 따라 카테고리를 분류합니다.
    지역명은 1개만 있거나, 출발지와 도착지 정보 2개가 있는 경우로 나뉩니다.
    사용자가 원하는 정보가 '날씨','교통','맛집' 중에 어떤 카테고리인지 파악합니다.
    json 형식으로 출력합니다.
    1. 지역명 (1개인 경우)
    2. 출발지와 도착지 지역명 (2개인 경우)
    3. 카테고리
    """
    
    # API 호출
    response = call_gpt_api(model, prompt, utterance)
    
    # Response 처리
    if response is not None:
        try:
            result = json.loads(response.choices[0].message.content) #[8:-4]
            return result
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            return None
    else:
        print("API 응답이 없습니다.")
        return None

