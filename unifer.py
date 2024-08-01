import io
from PIL import Image
import requests
import base64
import numpy as np


def add_random_noise(image, noise_level=2):
    """ Функция для добавления шума на изображение """
    image_array = np.array(image)
    height, width, channels = image_array.shape
    noise = np.random.randint(-noise_level, noise_level + 1, (height, width, channels))
    noisy_image_array = image_array + noise
    noisy_image_array = np.clip(noisy_image_array, 0, 255)
    noisy_image = Image.fromarray(noisy_image_array.astype('uint8'))
    return noisy_image


def creating_image_copy(image_path: str, count_copy: int) -> list:
    """ Функция для создания уникальных копий фото """
    image = Image.open(image_path)
    image = delete_exif(image)    # удаление метаданных
    images = []    # список с полученными фото
    for i in range(count_copy):
        images.append(add_random_noise(image))

    return images


def delete_exif(image):
    """ Функция для удаления метаданных фото """
    data = list(image.getdata())    # получение метаданных
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    return image_without_exif


def hosting_images(images: list[Image], secret_key: str, last_index=0) -> dict:
    """ Функция для хостинга списка фото """
    image_links = []
    images_error = []    # список для фото и их номеров, которые не удалось подгрузить
    upload_url = 'https://api.imgbb.com/1/upload'
    for i, image in enumerate(images):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_byte = buffered.getvalue()
        image64 = base64.b64encode(img_byte).decode('utf-8')
        params = {
            "key": secret_key,
            "image": image64,
            "name": f'{last_index + i}_image'
        }
        response = requests.post(upload_url, params)
        if response.status_code == 200:
            image_links.append(response.json()['data']['image']['url'])
        elif response.status_code == 400:
            print("Токен не действительный")
            return {
                'msg': 'ERROR: invalid token',
                'data': 0 if i == 0 else i - 1,
            }
        else:
            images_error.append(image)
    print(f'Не загружено {len(images_error)} фотографий')
    if images_error:
        hosting_images(images_error,secret_key, len(images))
    return {
        'msg': "ok",
        'data': image_links,
    }


def all_program_func(count: int, image_path: str, key: str):
    """ Функция выполняющая полноценный комплекс программы """
    image_list = creating_image_copy(image_path, count)
    host_result = hosting_images(image_list, key)
    return host_result
