import requests

def download_image(image_url):
    """загружать изображение по url в бинарном виде"""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки изображения: {e}")


def save_image(image_data, filepath):
    """сохраняем бинарные данные изображения в файл"""
    try:
        with open(filepath, 'wb') as file:
            file.write(image_data)
        print(f"Изображение успешно сохранено в: {filepath}")
    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")


def main():
    """основная программа"""
    image_url = input("Введите URL-адрес изображения: ")
    image_data = download_image(image_url)

    if image_data:
        filepath = input("Введите путь для сохранения файла (например, image.jpg): ")
        save_image(image_data, filepath)



if __name__ == "__main__":
   main()
