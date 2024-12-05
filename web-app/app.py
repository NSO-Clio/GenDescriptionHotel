from flask import Flask, request, render_template, jsonify
from model import DescriptionGener
from data_knowledge import DataKnowLedge
from get_geo import InfoGeo
import conf
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict


# Инициализация Flask-приложения и модели генерации описаний
app: Flask = Flask(__name__, static_folder='static', static_url_path='/static')
llm: DescriptionGener = DescriptionGener()
dk: DataKnowLedge = DataKnowLedge()
info_geo: InfoGeo = InfoGeo(api_key=conf.API_KEY_GOOGLE_MAPS, radius=2000)

# Настройка логирования
handler = RotatingFileHandler('application.log', maxBytes=1_000_000, backupCount=5, encoding="utf-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


def get_similar_des(text: str) -> Any:
    similar_des: list = dk.get_similar_chunks(query=text)
    similar_des: dict = {i: similar_des[i] for i in range(len(similar_des))}
    return jsonify(similar_des)


@app.route('/')
def main() -> str:
    """Главная страница приложения."""
    return render_template('welcome.html')


@app.route('/generate')
def generate() -> str:
    """Страница для ввода данных для генерации описания отеля."""
    return render_template('index.html')


@app.route('/get_data', methods=['POST'])
def get_data() -> Any:
    """
    Обработка данных, полученных от клиента для генерации описания отеля.
    Ожидается JSON с информацией об отеле.
    
    Возвращает:
        JSON-ответ с описанием отеля или ошибкой, если данные некорректны.
    """
    data: Dict[str, Any] = request.get_json()  # Получение JSON-данных от клиента
    
    # Извлечение данных об отеле из запроса
    hotel_name: str = data.get('hotelName', '')
    hotel_address: str = data.get('hotelAddress', '')
    price_per_night: str = data.get('pricePerNight', '')
    category: str = data.get('category', '')
    services: str = data.get('services', '')
    features: str = data.get('features', '')

    print("Received data:", data)  # Логирование полученных данных

    # Генерация описания отеля с использованием модели
    response_text: str = llm.genDescription(
        hotel_name=hotel_name,
        hotel_address=hotel_address,
        average_price=price_per_night,
        target_category=category,
        services_description=services,
        hotel_features=features
    )

    print("Generated description:", response_text)  # Логирование результата генерации
    app.logger.info(
        f"hotel_name:{hotel_name} "
        f"hotel_address:{hotel_address} "
        f"price_per_night:{price_per_night} "
        f"category:{category} "
        f"services:{services} "
        f"features:{features} "
        f"Generated description:{response_text}"
    )
    # Возврат JSON-ответа с сгенерированным описанием
    return jsonify({"description": response_text})


@app.route('/generate_description', methods=['POST'])
def generate_description() -> Any:
    data: Dict[str, Any] = request.get_json()  # Получение JSON-данных от клиента
    print("Received data:", data)

    # Извлечение данных об отеле из запроса
    hotel_name: str = data.get('hotelName', '')
    addres: str = data.get('hotelAddres', '')
    category: str = data.get('category', '')
    services: str = data.get('services', '')
    features: str = data.get('features', '')

    attractions: dict = info_geo.get_attractions(addres)
    info_geo_attractions: str = ''
    for name, details in attractions.items():
        info_geo_attractions += f"{name}: Рейтинг - {details['rating']}, Расстояние - {details['distance']} \n"
    app.logger.info(
        f"get_geo_info: {addres} "
        f"info: {info_geo_attractions}"
    )

    similar_descriptions: str = dk.get_similar_chunks(
        f"hotel_name:{hotel_name} "
        f"category:{category} "
        f"services:{services} "
        f"features:{features + f' близко к Достопримечательностям: {info_geo_attractions}'} ",
        k=3
    )

    description1: str = llm.genDescription(
        hotel_name=hotel_name,
        target_category=category,
        services_description=services,
        hotel_features=features + f' близко к Достопримечательностям: {info_geo_attractions}',
        similar_des = similar_descriptions,
        temperature=0.2
    )
    app.logger.info(
        f"hotel_name:{hotel_name} "
        f"category:{category} "
        f"services:{services} "
        f"features:{features + f' близко к Достопримечательностям: {info_geo_attractions}'} "
        f"Generated description:{description1}"
    )

    description2: str = llm.genDescription(
        hotel_name=hotel_name,
        target_category=category,
        services_description=services,
        hotel_features=features + f' близко к Достопримечательностям: {info_geo_attractions}',
        similar_des = similar_descriptions,
        temperature=1.0
    )
    app.logger.info(
        f"hotel_name:{hotel_name} "
        f"category:{category} "
        f"services:{services} "
        f"features:{features + f' близко к Достопримечательностям: {info_geo_attractions}'} "
        f"Generated description:{description2}"
    )
    
    # return jsonify({'description1': 'description1_1', 'description2': 'description2_2'})
    return jsonify({'description1': description1, 'description2': description2})


@app.route('/save_choice', methods=['POST'])
def save_choice():
    data = request.get_json()
    choice = data.get('choice')
    # Сохраняем выбор пользователя в базу данных или журнал
    print(f"Пользователь выбрал: {choice}")
    return jsonify({"message": f"Выбор {choice} сохранен успешно"})


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    print(data)

    category: str = data.get('category', '')
    description: str = data.get('description', '')
    rating: str = data.get('rating', '')
    comment: str = data.get('comment', '')

    response_text: str = f'Катигория: {category} \n Описание: {description} \n Оценка: {rating} \n Комментарий: {comment}'
    dk.add_chunks([response_text])
    app.logger.info(f'comment:{response_text}')
    return jsonify({'message': 'Отзыв сохранён!'})


# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
