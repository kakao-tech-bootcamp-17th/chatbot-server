from flask import Flask, jsonify, request, current_app
from openai import OpenAI
from . import gpt_bp
import json
from app.weather.service.weather_service import WeatherService
from app.traffic.service.traffic_service import TrafficService
from app.local.service.local_service import LocalService

# Debugging Package
# import time
import os
from datetime import datetime

# 채팅 모델 컨텍스트
CHAT_MODEL_CONTEXT = '''
    당신은 사용자 발화로부터 지역명, 키워드를 추출하고, 어떤 정보가 필요한지에 따라 카테고리를 분류합니다.
    지역명은 1개만 있거나, 출발지와 도착지 정보 2개가 있는 경우로 나뉩니다.
    사용자가 원하는 정보가 '날씨','교통','지도' 중에 어떤 카테고리인지 파악합니다.
    키워드는 카테고리가 '지도' 인 경우 지도에서 검색할 키워드 (예 맛집, 카페, 중국집, 주차장 등등)
    json 형식으로 출력합니다.
    1. 지역명 (1개인 경우)
    2. 출발지와 도착지 지역명 (2개인 경우)
    3. 카테고리
    4. 키워드 (카테고리가 '지도'인 경우)
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
    print(pre_response_message)
 
    pre_response_data = json.loads(pre_response_message.content)
    category = pre_response_data.get("카테고리")
    response = ""
    
    # 교통 프롬프트 후처리 
    if category == "교통" :
        start = pre_response_data.get("출발지")
        goal = pre_response_data.get("도착지")

        traffic_service = TrafficService()
        traffic_info = traffic_service.find_direction(start, goal)

        traffic_prompt = f'''
        {traffic_info}로부터 '거리', '소요시간', '유류비', '택시비', '톨비' 정보를 찾아
        {utterance}에 대해 뉴스 아나운서처럼 대답하시오.
        '''
        
        print(traffic_prompt)
        
        messageList = [{"role": "system", "content": traffic_prompt}]
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
        return jsonify(response)

    # 날씨 프롬프트 후처리
    if category == "날씨" :
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
        {utterance}에 대해서 아나운서처럼 대답을 해줘
        '''
        
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
        return jsonify(response)
        
    if category == "지도" :
        location = pre_response_data.get("지역명")
        keyword = pre_response_data.get("키워드")
        map_service = LocalService()
        map_info = map_service.search_places(location, keyword)

        prompt = f'''
        {map_info}를 참고해서
        가장 추천하는 장소의 거리와 이름을 2곳 알려줘
        '''

        messageList = [{"role": "system", "content": prompt}]
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
        return jsonify(response)
    
    return jsonify(response)