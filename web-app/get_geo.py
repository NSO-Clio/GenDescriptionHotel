import requests


class InfoGeo:
    def __init__(self, api_key: str, radius: int = 2000) -> None:
        """
        Инициализация класса InfoGeo.

        Параметры:
            api_key (str): Ключ API для Google Maps.
            radius (int): Радиус поиска (в метрах). По умолчанию — 2000.
        """
        self.api_key: str = api_key
        self.radius: int = radius

    def get_coordinates_from_address(self, address: str) -> tuple[float | None, float | None]:
        if not address.strip():
            print("Адрес не указан или пуст.")
            return None, None

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self.api_key,
            "language": "ru"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print("Координаты не  найдены.")
                return None, None
        else:
            print(f"Ошибка API: {response.status_code}, {response.text}")
            return None, None

    def get_nearby_places(self, latitude: float, longitude: float) -> list[dict]:
        """
        Получение списка достопримечательностей рядом с указанными координатами.

        Параметры:
            latitude (float): Широта.
            longitude (float): Долгота.

        Возвращает:
            list[dict]: Список достопримечательностей.
        """
        if latitude is None or longitude is None:
            print("Не удалось получить координаты.")
            return []

        url: str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params: dict[str, str | int] = {
            "location": f"{latitude},{longitude}",
            "radius": self.radius,
            "type": "tourist_attraction",
            "key": self.api_key,
            "language": "ru"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data: dict = response.json()
            return data.get('results', [])
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return []

    def get_distance_to_place(
        self, 
        place_lat: float, 
        place_lng: float, 
        latitude: float, 
        longitude: float
    ) -> tuple[str, float]:
        """
        Получение расстояния от заданного адреса до указанной точки.

        Параметры:
            place_lat (float): Широта достопримечательности.
            place_lng (float): Долгота достопримечательности.
            latitude (float): Широта текущего адреса.
            longitude (float): Долгота текущего адреса.

        Возвращает:
            tuple[str, float]: Текст расстояния и значение в метрах.
        """
        url: str = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params: dict[str, str] = {
            "origins": f"{latitude},{longitude}",
            "destinations": f"{place_lat},{place_lng}",
            "key": self.api_key,
            "language": "ru"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data: dict = response.json()
            if data['rows'] and data['rows'][0]['elements']:
                element: dict = data['rows'][0]['elements'][0]
                distance_text: str = element.get('distance', {}).get('text', 'Нет данных')
                distance_value: float = element.get('distance', {}).get('value', float('inf'))
                return distance_text, distance_value
        return 'Нет данных', float('inf')

    def get_attractions(self, address: str, top: int = 10) -> dict[str, dict[str, str | float]]:
        """
        Получение отсортированного по рейтингу списка достопримечательностей с расстояниями.

        Параметры:
            address (str): Адрес для поиска достопримечательностей.
            top (int): Количество лучших результатов. По умолчанию — 3.

        Возвращает:
            dict[str, dict[str, str | float]]: Словарь достопримечательностей с их характеристиками.
        """
        latitude, longitude = self.get_coordinates_from_address(address)
        places: list[dict] = self.get_nearby_places(latitude, longitude)

        if not places:
            print("Достопримечательности не найдены.")
            return {}

        attractions: dict[str, dict[str, str | float]] = {}

        for place in places[:top]:
            name: str = place['name']
            rating: float | str = place.get('rating', 'Нет рейтинга')
            location: dict = place['geometry']['location']
            distance_text, distance_value = self.get_distance_to_place(location['lat'], location['lng'], latitude, longitude)

            if distance_value <= self.radius:
                attractions[name] = {
                    'rating': rating,
                    'distance': distance_text
                }

        return dict(sorted(attractions.items(), key=lambda item: item[1]['rating'], reverse=True))


# city = "Санкт-Петербур"
# street = "набережная реки Фонтанки, 22"
# # address = f'{city}, {street}'
# address = 'Москва, ул.Большая Якиманка, д.1'
# api_key = "API_KEY_GOOGLE_MAPS"

# geo_info = InfoGeo(api_key)
# print(f"Адрес: {address}")
# attractions = geo_info.get_attractions(address)

# if attractions:
#     print("Достопримечательности рядом:")
#     for name, details in attractions.items():
#         print(f"{name}: Рейтинг - {details['rating']}, Расстояние - {details['distance']}")
# else:
#     print("Достопримечательностей не найдено.")