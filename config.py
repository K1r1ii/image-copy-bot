from dotenv import load_dotenv
import os

load_dotenv()  # получаем данные в переменных окружения
TOKEN = os.environ.get('TOKEN')
START_ANSWER = 'Привет! Я бот, который поможет с твоей работой!\nОтправь мне клюс для хоста т начнем работу!'
HELP_MSG = 'Инструкция:\nДля старта работы введи сообщение "Начать работу" либо выбери соответствующую кнопку в меню.\n' \
           'Далее следуй инструкциям от бота: отправь токен с сайта (ВАЖНО! Он должен быть действительным)\n' \
           'Фото отправляй, как обычное вложение, отправлять как документ не требуется\n' \
           'При вводе данных не пиши ничего лишнего, иначе бот тебя не поймет и сообщит об этом.\n' \
           'Ссылки на фото бот пришлет в виде текстового документа с названием links.txt\n' \
           'На этом все, приятного пользования!'
INVALID_TOKEN = 'Ошибка с токеном. Либо введен не корректный токен, либо истек срок действия токена.'
