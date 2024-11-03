from flask import Flask, request, render_template, jsonify
from model import DescriptionGener


app = Flask(__name__, static_folder='static', static_url_path='/static')
llm = DescriptionGener()


@app.route('/')
def main():
    return render_template('welcome.html')

@app.route('/generate')
def generate():
    return render_template('index.html')


@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    hotel_name = data.get('hotelName')
    hotel_address = data.get('hotelAddress')
    price_per_night = data.get('pricePerNight')
    category = data.get('category')
    services = data.get('services')
    features = data.get('features')
    print(data)
    # Генерация описания с использованием модели
    response_text = llm.genDescription(
        hotel_name=hotel_name,
        hotel_address=hotel_address,
        average_price=price_per_night,
        target_category=category,
        services_description=services,
        hotel_features=features
    )
    print(response_text)
    # Возврат JSON с описанием
    return jsonify({"description": response_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
