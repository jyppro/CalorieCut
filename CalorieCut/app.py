import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_food_by_calories(calories):
    api_key = '09c2df3a37c248089dd8'
    api_endpoint = 'http://openapi.foodsafetykorea.go.kr/api/'

    try:
        # API 요청에 필요한 URL 조립
        request_url = f"{api_endpoint}{api_key}/COOKRCP01/json/1/500"
        
        # API에 GET 요청을 보내고 응답을 받습니다.
        response = requests.get(request_url)
        
        if response.status_code == 200:
            data = response.json()
            # 실제 API에서 필요한 데이터를 추출하여 반환합니다.
            all_foods = data['COOKRCP01']['row']
            
            # 서버에서 받은 칼로리 값을 이용하여 해당하는 음식을 필터링합니다.
            similar_foods = []
            for food in all_foods:
                # 실수로 변환하여 비교합니다.
                if abs(float(food['INFO_ENG']) - float(calories)) < 50:  # 예시로 50의 차이 이내로 유사한 값이라 가정합니다.
                    similar_foods.append(food)
            
            return similar_foods
        else:
            return []  # 오류가 발생했을 경우 빈 리스트 반환
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return []



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # POST 요청으로부터 칼로리 값 받기
        total_calories = int(request.form['calories'])

        # 각 식사에 해당하는 칼로리 값을 이용해 음식 정보를 가져옴
        breakfast_calories = int(total_calories * 0.25)
        lunch_calories = int(total_calories * 0.4)
        dinner_calories = int(total_calories * 0.35)

        breakfast_foods = get_food_by_calories(breakfast_calories)
        lunch_foods = get_food_by_calories(lunch_calories)
        dinner_foods = get_food_by_calories(dinner_calories)

        return jsonify({
            'breakfast_foods': breakfast_foods,
            'lunch_foods': lunch_foods,
            'dinner_foods': dinner_foods
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
