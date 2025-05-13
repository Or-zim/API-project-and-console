import requests as rq
API_KEY ='4a620c1e18c06542c236b9792393dd7f'
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """получение данных из get запроса"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = rq.get(BASE_URL, params=params)
    return response


def process_weather_data(response):
    """Обрабатывает объект ответа и возвращает нужные данные"""
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return temperature, description
    else:
        response.raise_for_status()


def main():
    """основная программа"""
    city = input("Введите название города: ")
    try:
        response = get_weather_data(city)
        temperature, description = process_weather_data(response)
        print(response)
        print(f"Погода в городе {city}:")
        print(f"Температура: {round(temperature)}°C")
        print(f"Описание: {description}")
    except rq.exceptions.RequestException as e:
        print(f'Ошибка: {e}')


if __name__ == "__main__":
    main()
