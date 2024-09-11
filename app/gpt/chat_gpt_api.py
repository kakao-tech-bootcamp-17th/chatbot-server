from flask import Flask, jsonify, request, current_app
from openai import OpenAI
from . import gpt_bp
import json
from app.weather.service.weather_service import WeatherService
from app.local.service.local_service import LocalService
from app.local.dto.response.place_info_response_dto import PlaceInfoResponseDto

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

    if category == "날씨" : 
        weather_service = WeatherService()
        weather_info = weather_service.get_weather_by_address(city)

        temperature = weather_info.weather.temperature
        description = weather_info.weather.description
        feels_like = weather_info.weather.feels_like
        humidity = weather_info.weather.humidity
        city = weather_info.weather.city

        weather_prompt = f'''
        {weather_info}

        위의 정보들 중에서 적당한 정보들을 이용해서
        {utterance} 에 대한 대답을 해줘
        수치들은 정수로 표현하고 아나운서들이 말하듯이 매끄럽게 말해줘
        '''

        print(weather_prompt)

    '''
    if category == "맛집" :
        map_service = LocalService()
        map_info = map_service.search_places(city)

        place = map_info.PlaceInfoResponseDto.place_name
        distance = map_info.PlaceInfoResponseDto.distance

        print(f"장소명 : {place}")

        map_prompt = f
        장소명 : {place}
        거리 : {distance}




        

    if category == "교통" :

'''
    
    messageList = [{"role": "system", "content": weather_prompt}]
    dicMessage = {"role": "user", "content": utterance}
    messageList.append(dicMessage)

    post_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messageList
    )
    post_response_message = post_completion.choices[0].message
    
    print(post_response_message.content)

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
    return jsonify(response)