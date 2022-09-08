from aiogram import types


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Купить', callback_data='buy')
    btn2 = types.InlineKeyboardButton('Продать', callback_data='sell')
    btn3 = types.InlineKeyboardButton('О сервисе', callback_data='about')
    btn4 = types.InlineKeyboardButton('Калькулятор валют', callback_data='calculator')
    btn5 = types.InlineKeyboardButton('Отзывы', callback_data='review')
    btn6 = types.InlineKeyboardButton('Как обменять?', callback_data='how')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6)

    return kb


def inline_markup_moderator_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Курс BTC', callback_data='btc_rate')
    btn2 = types.InlineKeyboardButton('Курс ETH', callback_data='eth_rate')
    btn3 = types.InlineKeyboardButton('Курс LTC', callback_data='ltc_rate')
    btn4 = types.InlineKeyboardButton('Курс XMR', callback_data='xmr_rate')
    btn5 = types.InlineKeyboardButton('Адрес BTC', callback_data='btc_address')
    btn6 = types.InlineKeyboardButton('Адрес ETH', callback_data='eth_address')
    btn7 = types.InlineKeyboardButton('Адрес LTC', callback_data='ltc_address')
    btn8 = types.InlineKeyboardButton('Адрес XMR', callback_data='xmr_address')
    btn9 = types.InlineKeyboardButton('Тинькофф', callback_data='reqs_tinkoff')
    btn10 = types.InlineKeyboardButton('Банк Открытие', callback_data='reqs_open_bank')
    btn11 = types.InlineKeyboardButton('Киви карта', callback_data='reqs_qiwi')
    btn12 = types.InlineKeyboardButton('Раздел "О сервисе"', callback_data='about')
    btn13 = types.InlineKeyboardButton('Раздел "Как обменять?"', callback_data='how')
    btn14 = types.InlineKeyboardButton('Рассылка пользователям', callback_data='sharing')
    btn15 = types.InlineKeyboardButton('Cписок пользователей', callback_data='users_list')
    btn16 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16)

    return kb


def inline_markup_buy():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('RUB-BTC', callback_data='rub-btc')
    btn2 = types.InlineKeyboardButton('RUB-LTC', callback_data='rub-ltc')
    btn3 = types.InlineKeyboardButton('RUB-ETH', callback_data='rub-eth')
    btn4 = types.InlineKeyboardButton('RUB-XMR', callback_data='rub-xmr')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_markup_sell():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('BTC-RUB', callback_data='btc-rub')
    btn2 = types.InlineKeyboardButton('LTC-RUB', callback_data='ltc-rub')
    btn3 = types.InlineKeyboardButton('ETH-RUB', callback_data='eth-rub')
    btn4 = types.InlineKeyboardButton('XMR-RUB', callback_data='xmr-rub')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_markup_calculator():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('RUB-BTC', callback_data='rub-btc')
    btn3 = types.InlineKeyboardButton('RUB-LTC', callback_data='rub-ltc')
    btn5 = types.InlineKeyboardButton('RUB-ETH', callback_data='rub-eth')
    btn7 = types.InlineKeyboardButton('RUB-XMR', callback_data='rub-xmr')

    btn2 = types.InlineKeyboardButton('BTC-RUB', callback_data='btc-rub')
    btn4 = types.InlineKeyboardButton('LTC-RUB', callback_data='ltc-rub')
    btn6 = types.InlineKeyboardButton('ETH-RUB', callback_data='eth-rub')
    btn8 = types.InlineKeyboardButton('XMR-RUB', callback_data='xmr-rub')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    return kb


def reply_markup_payment_type():
    kb = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)

    btn1 = types.KeyboardButton('Тинькофф')
    btn2 = types.KeyboardButton('Банк Открытие')
    btn3 = types.KeyboardButton('Киви карта')
    btn4 = types.KeyboardButton('Отмена')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def reply_markup_is_paid():
    kb = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

    btn1 = types.KeyboardButton('Отмена')
    btn2 = types.KeyboardButton('Я оплатил(а)')

    kb.add(btn1, btn2)

    return kb


def reply_markup_is_correct():
    kb = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

    btn1 = types.KeyboardButton('Отмена')
    btn2 = types.KeyboardButton('Верно, продолжить')

    kb.add(btn1, btn2)

    return kb


def reply_markup_call_off(text):
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text=text)

    kb.add(btn1)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + ' ↩️', callback_data='back')

    kb.add(btn1)

    return kb


def inline_markup_check_request():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('ОБРАБОТАТЬ ЗАЯВКУ', callback_data='check_request')

    kb.add(btn1)

    return kb


def inline_markup_request_opps():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Одобрить заявку ✅', callback_data='approve')
    btn2 = types.InlineKeyboardButton('Отклонить заявку ❌', callback_data='reject')

    kb.add(btn1, btn2)

    return kb


def inline_markup_book_opps():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Посмотреть отзывы 👁‍🗨', callback_data='check_reviews')
    btn2 = types.InlineKeyboardButton('Написать отзыв ✍', callback_data='write_review')
    btn3 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2, btn3)

    return kb


def inline_markup_check_review():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('ОБРАБОТАТЬ ОТЗЫВ', callback_data='handle_review')

    kb.add(btn1)

    return kb


def inline_markup_review_opps():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Добавить в книгу отзывов ✅', callback_data='approve')
    btn2 = types.InlineKeyboardButton('Отклонить отзыв ❌', callback_data='reject')
    btn3 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')

    kb.add(btn1, btn2), btn3

    return kb
