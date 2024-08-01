from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from config import TOKEN, START_ANSWER, HELP_MSG, INVALID_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from keyboards import get_keyboard
from unifer import all_program_func

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class GetImages(StatesGroup):
    """ Класс с состояниями бота """
    get_key = State()    # получение ключа
    get_count_copy = State()    # получение кол-ва копий
    get_image = State()    # получение изображения


def create_txt_doc(links: list[str]) -> None:
    """ Функция для записи ссылок в документ """
    with open('links.txt', 'w') as f:
        f.write('\n'.join(links))


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    """ Обработка стартовой команды """
    await message.answer(text=START_ANSWER, reply_markup=get_keyboard())


@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def help_cmd(message: types.Message) -> None:
    """ Функция для команды помощь """
    await message.answer(HELP_MSG)


@dp.message_handler(Text(equals='Начать работу', ignore_case=True), state=None)
async def start_work(message: types.Message) -> None:
    """ Функция запускающая цикл программы """
    await GetImages.get_key.set()
    await message.answer('Отправь мне ключ к своему api')


@dp.message_handler(state=GetImages.get_key)
async def load_key(message: types.Message, state: FSMContext):
    """ Обработка получения ключа для API """
    async with state.proxy() as data:
        data['key'] = message.text
    await GetImages.next()
    await message.answer('Теперь напиши, сколько копий нужно?')


@dp.message_handler(state=GetImages.get_count_copy)
async def load_count_copy(message: types.Message, state: FSMContext):
    """ Обработка получения кол-ва копий """
    try:
        async with state.proxy() as data:
            data['count_copy'] = int(message.text)
        await GetImages.next()
        await message.answer('Теперь отправь фото (простым вложением - не документом)')
    except ValueError:
        await GetImages.get_count_copy.set()
        await message.answer('Некорректно введено количество фото, напишите еще раз ЧИСЛО')


# проверяем корректность отправки фото
@dp.message_handler(lambda message: not message.photo, state=GetImages.get_image)
async def check_image(message: types.Message):
    """ Проверка корректности отправленного фото """
    return await message.reply('Это не фото')


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=GetImages.get_image)
async def load_image(message: types.Message, state: FSMContext):
    """ Обработка отправленного фото """
    # получение всех данных от пользователя
    async with state.proxy() as data:
        count_copy = data['count_copy']
        key = data['key']
    await message.answer('Супер, начинаю работу, нужно немного подождать...')

    # работа с фото (сохранение, обработка)
    photo = message.photo[-1]
    file_path = await photo.download(destination_file='image.jpg')

    # получение списка ссылок (запуск программы по созданию копий)
    result = all_program_func(count_copy, file_path.name, key)

    # проверка полученных данных
    if result['msg'] != 'ok':
        await message.answer(INVALID_TOKEN + f' Успешно загружено {result["data"]} фотографий')
        await state.finish()
    else:
        create_txt_doc(result['data'])
        await message.answer('Готово! Лови документ с ссылками:')
        await message.answer_document(InputFile('links.txt'))
        await state.finish()


# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
