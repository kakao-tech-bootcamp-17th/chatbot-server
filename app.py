from flask import Flask, request
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

KAKAO_REQEUST_URL="https://apis-navi.kakaomobility.com/v1/directions"

@app.route("/finding-way", methods=['GET'])
def findWay():
    kakao_api_key = os.getenv("KAKAO_APP_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    print(kakao_api_key)
    
    origin_x = request.args.get("origin_x")
    origin_y = request.args.get("origin_y")
    origin_name = request.args.get("origin_name", None)
    dest_x = request.args.get("dest_x")
    dest_y = request.args.get("dest_y")
    dest_name = request.args.get("dest_name", None)

    # `origin`은 다음 중 하나의 형식으로 요청:
    # ${X좌표},${Y좌표},name=${출발지명} 또는
    # ${X좌표},${Y좌표}
    origin = f"{origin_x},{origin_y}"
    if origin_name is not None:
        origin += f",name={origin_name}"
    dest = f"{dest_x},{dest_y}"
    if dest_name is not None:
        dest += f",name={dest_name}"
    
    params = {
        "origin": origin,
        "destination": dest
    }

    request_url =KAKAO_REQEUST_URL
    response = requests.get(KAKAO_REQEUST_URL, headers=headers, params=params)

    data = response.json()

    return data

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)