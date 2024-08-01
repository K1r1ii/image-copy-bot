from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# клавиатура для управления
def get_keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура для пользователя """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Начать работу')
    b2 = KeyboardButton('Помощь')
    kb.row(b1, b2)
    return kb
