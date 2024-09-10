from flask import Flask, jsonify, request, current_app
from openai import OpenAI
from . import gpt_bp
import json
from datetime import datetime
from app.weather.service.weather_service import WeatherService

# 채팅 모델 컨텍스트
CHAT_MODEL_CONTEXT = '''
    당신은 사용자 발화로부터 지역명을 추출하고, 어떤 정보가 필요한지에 따라 카테고리를 분류합니다.
    지역명은 1개만 있거나, 출발지와 도착지 정보 2개가 있는 경우로 나뉩니다.
    사용자가 원하는 정보가 '날씨','교통','맛집' 중에 어떤 카테고리인지 파악합니다.
    json 형식으로 출력합니다.
    1. 지역명 (1개인 경우)
    2. 출발지와 도착지 지역명 (2개인 경우)
    3. 카테고리
    '''
    
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
    pre_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messageList
    )
    pre_response_message = pre_completion.choices[0].message

    pre_response_data = json.loads(pre_response_message.content)
    category = pre_response_data.get("카테고리")
    city = pre_response_data.get("지역명")

    weather_service = WeatherService()
    weather_info = weather_service.get_weather_by_address(city)

    temperature = weather_info.weather.temperature
    description = weather_info.weather.description
    feels_like = weather_info.weather.feels_like
    humidity = weather_info.weather.humidity
    city = weather_info.weather.city

    weather_prompt = f'''
    지역 : {city}  
    기온 : {temperature} 
    체감온도 : {feels_like}
    습도 : {humidity}
    날씨 : {description}

    위의 정보를 이용해서
    {utterance}에 대한 대답을 해줘
    '''
    
    print(weather_prompt)
    
    messageList = [{"role": "system", "content": weather_prompt}]
    dicMessage = {"role": "user", "content": utterance}
    messageList.append(dicMessage)

    post_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messageList
    )
    post_response_message = post_completion.choices[0].message
    
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{post_response_message.content}"
                    }
                }
            ]
        }
    }
    print("테스트용 확인 TimeSleep ------------------------")
    time.sleep(2)
    now = datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
    txtFileName = datetime.now().strftime('%Y%m%d%H%M%S')
    log = f"{now} -- \nresponse : {response}"
    with open(f"../log/{txtFileName}.txt", 'w') as file :
        file.write(log)
    return jsonify(response)