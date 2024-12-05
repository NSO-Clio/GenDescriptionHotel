import requests


class InfoGeo:
    def __init__(self, address, api_key, radius=2000):
        self.api_key = api_key
        self.radius = radius
        self.address = address
        self.latitude, self.longitude = self.get_coordinates_from_address()

    def get_coordinates_from_address(self):
        """Получает координаты (широта и долгота) по указанному адресу."""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": self.address,
            "key": self.api_key,
            "language": "ru"  # Язык результата
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print("Координаты не найдены.")
                return None, None
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None, None

    def get_nearby_places(self):
        """Получает список достопримечательностей рядом с заданными координатами."""
        if not self.latitude or not self.longitude:
            print("Координаты не заданы.")
            return []

        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{self.latitude},{self.longitude}",
            "radius": self.radius,
            "type": "tourist_attraction",  # Тип для поиска достопримечательностей
            "key": self.api_key,
            "language": "ru"  # Язык результата
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return []

    def get_distance_to_place(self, place_lat, place_lng):
        """Получает расстояние от текущего адреса до указанной точки."""
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": f"{self.latitude},{self.longitude}",
            "destinations": f"{place_lat},{place_lng}",
            "key": self.api_key,
            "language": "ru"  # Язык результата
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['rows'] and data['rows'][0]['elements']:
                element = data['rows'][0]['elements'][0]
                distance_text = element.get('distance', {}).get('text', 'Нет данных')
                distance_value = element.get('distance', {}).get('value', float('inf'))
                return distance_text, distance_value
        return 'Нет данных', float('inf')

    def get_attractions(self):
        """Возвращает отсортированный по рейтингу словарь достопримечательностей с расстояниями."""
        places = self.get_nearby_places()
        if not places:
            print("Достопримечательности не найдены.")
            return {}

        attractions = {}
        for place in places:
            name = place['name']
            rating = place.get('rating', 'Нет рейтинга')
            location = place['geometry']['location']
            distance_text, distance_value = self.get_distance_to_place(location['lat'], location['lng'])
            if distance_value <= 2000:  # Фильтр по расстоянию до 2 км
                attractions[name] = {
                    'rating': rating,
                    'distance': distance_text
                }

        return dict(sorted(attractions.items(), key=lambda item: item[1]['rating'], reverse=True))
