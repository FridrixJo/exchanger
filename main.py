import asyncio
import time

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from aiogram import types
import random
import string
from config import *
from key_boards import *
from FSMClasses import *
from urllib import request


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data_base.db_users import UsersDB
from data_base.db_statement import StatementDB
from data_base.db_requests import RequestDB


storage = MemoryStorage()

bot = Bot(TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(ADMIN_ID)]


users_db = UsersDB('data_base/exchanger.db')
statement_db = StatementDB('data_base/exchanger.db')
requests_db = RequestDB('data_base/exchanger.db')


BACK_BTN = types.InlineKeyboardButton('Назад ↩️', callback_data='back')


LEFT_LIMIT = 1000
RIGHT_LIMIT = 500000


async def clear_state(state: FSMContext):
    try:
        current_state = state.get_state()
        if current_state is not None:
            await state.finish()
    except Exception as error:
        print(error)


def check(url):
    try:
        request.urlopen(url)
        return True
    except Exception as e:
        return False


def get_name(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    name = ''
    if first_name is not None:
        name += first_name
        name += ' '
    if last_name is not None:
        name += last_name
        name += ' '
    if username is not None:
        name += '@'
        name += username

    return name


async def send_menu(message: types.Message):
    text = 'Главное меню'
    await bot.send_message(message.chat.id, text=text, reply_markup=inline_markup_menu())


async def edit_to_menu(message: types.Message):
    text = 'Главное меню'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_menu())


async def send_moderator_menu(message: types.Message):
    text = 'Главное меню модератора'
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=inline_markup_moderator_menu())


async def edit_to_moderator_menu(message: types.Message):
    text = 'Главное меню модератора'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_moderator_menu())


@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMUser.input_quantity, FSMUser.get_reqs, FSMUser.get_rub_payment, FSMUser.is_correct, FSMUser.is_paid, FSMUser.get_amount])
async def cancel_handler(message: types.Message, state: FSMContext):
    await clear_state(state)
    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    await send_menu(message)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if not users_db.user_exists(message.chat.id):
        users_db.add_user(message.chat.id, get_name(message))

        text = f'Пользователь {str(users_db.get_name(message.chat.id))} перешел в бота'
        for i in ADMIN_IDS:
            await bot.send_message(chat_id=i, text=text)

    await send_menu(message)


@dispatcher.message_handler(commands=['moderator'], state=['*'])
async def start_moderator(message: types.Message, state: FSMContext):
    for i in ADMIN_IDS:
        if message.chat.id == i:
            await clear_state(state)
            await send_moderator_menu(message)
            await FSMAdmin.moderator_opps.set()


@dispatcher.callback_query_handler(state=FSMAdmin.moderator_opps)
async def start_moderator(call: types.CallbackQuery, state: FSMContext):
    pass


@dispatcher.callback_query_handler()
async def get_callback_menu(call: types.CallbackQuery):
    if call.data == 'buy':
        text = 'Какой обмен вас интресует?'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_buy().add(BACK_BTN))
        await FSMUser.buy.set()
    elif call.data == 'sell':
        text = 'Какой обмен вас интресует?'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_sell().add(BACK_BTN))
        await FSMUser.buy.set()
    elif call.data == 'about':
        pass
    elif call.data == 'calculator':
        text = 'Выберите направление'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_calculator().add(BACK_BTN))
        await FSMUser.calculator.set()
    elif call.data == 'review':
        pass
    elif call.data == 'how':
        pass
    elif call.data == 'check_request':
        for i in ADMIN_IDS:
            if call.message.chat.id == i:
                text = 'Скопируйте и отправьте сюда номер заявки'
                await bot.send_message(call.message.chat.id, text)
                await FSMModeratorReply.request_id.set()


@dispatcher.callback_query_handler(state=FSMUser.calculator)
async def calculate(call: types.CallbackQuery, state: FSMContext):
    if 'rub-' in call.data:
        async with state.proxy() as file:
            file['currency'] = call.data[4:]
            file['exchange_type'] = 'from_rub'

        text = 'Введите сумму в рублях'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMUser.get_amount.set()
    elif '-rub' in call.data:
        currency: str = call.data[:3]
        async with state.proxy() as file:
            file['currency'] = currency
            file['exchange_type'] = 'to_rub'

        text = f'Введите сумму в {currency.upper()}'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMUser.get_amount.set()



@dispatcher.message_handler(state=FSMUser.get_amount)
async def get_rubles(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        exchange_type = file['exchange_type']
        currency = file['currency']

    if exchange_type == 'from_rub':
        try:
            a = int(message.text)
            if a < 0:
                text = 'Число меньше нуля. Попробуйте еще раз'
                await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
                await FSMUser.get_amount.set()
            else:
                text = f'{message.text} RUB = '

                if currency == 'btc':
                    text += f'{round(a / statement_db.get_btc(), 6)} BTC'
                elif currency == 'eth':
                    text += f'{round(a / statement_db.get_eth(),6)} ETH'
                elif currency == 'ltc':
                    text += f'{round(a / statement_db.get_ltc(), 6)} LTC'
                elif currency == 'xmr':ccd
                    text += f'{round(a / statement_db.get_xmr(), 6)} XMR'

                await clear_state(state)
                await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
                await send_menu(message)

        except Exception as e:
            text = 'Что-то пошло не так. Введите число еще раз'
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMUser.get_amount.set()

    elif exchange_type == 'to_rub':
        try:
            a = float(message.text)
            if a < 0:
                text = 'Число меньше нуля. Попробуйте еще раз'
                await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
                await FSMUser.get_amount.set()
            else:
                text = f'{a} {currency.upper()} = '

                if currency == 'btc':
                    text += f'{int(a * statement_db.get_btc())} RUB'
                elif currency == 'eth':
                    text += f'{int(a * statement_db.get_eth())} RUB'
                elif currency == 'ltc':
                    text += f'{int(a * statement_db.get_ltc())} RUB'
                elif currency == 'xmr':
                    text += f'{int(a * statement_db.get_xmr())} RUB'

                await clear_state(state)
                await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
                await send_menu(message)

        except Exception as e:
            text = 'Что-то пошло не так. Введите число еще раз'
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMUser.get_amount.set()


@dispatcher.callback_query_handler(state=FSMUser.buy)
async def choose_shop(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    else:
        currency = ''
        text = 'Актуальный курс 1'

        if call.data == 'rub-btc':
            text += f' BTC = {statement_db.get_btc()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите получить в BTC' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_btc(), 6)} до {round(RIGHT_LIMIT/statement_db.get_btc(), 6)} BTC'
        elif call.data == 'rub-ltc':
            text += f' LTC = {statement_db.get_ltc()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите получить в LTC' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_ltc(), 6)} до {round(RIGHT_LIMIT/statement_db.get_ltc(), 6)} LTC'
        elif call.data == 'rub-eth':
            text += f' ETH = {statement_db.get_eth()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите получить в ETH' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_eth(), 6)} до {round(RIGHT_LIMIT/statement_db.get_eth(), 6)} ETH'
        elif call.data == 'rub-xmr':
            text += f' XMR = {statement_db.get_xmr()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите получить в XMR' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_xmr(), 6)} до {round(RIGHT_LIMIT/statement_db.get_xmr(), 6)} XMR'
        elif call.data == 'btc-rub':
            text += f' BTC = {statement_db.get_btc()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите отдать в BTC. Бот рассчитает, сколько вы получите в RUB' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_btc(), 6)} до {round(RIGHT_LIMIT/statement_db.get_btc(), 6)} BTC'
        elif call.data == 'ltc-rub':
            text += f' LTC = {statement_db.get_ltc()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите отдать в LTC. Бот рассчитает, сколько вы получите в RUB' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_ltc(), 6)} до {round(RIGHT_LIMIT/statement_db.get_ltc(), 6)} LTC'
        elif call.data == 'eth-rub':
            text += f' ETH = {statement_db.get_eth()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите отдать в ETH. Бот рассчитает, сколько вы получите в RUB' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_eth(), 6)} до {round(RIGHT_LIMIT/statement_db.get_eth(), 6)} ETH'
        elif call.data == 'xmr-rub':
            text += f' XMR = {statement_db.get_xmr()} RUB' + '\n\n'
            text += 'Введите сумму, которую хотите отдать в XMR. Бот рассчитает, сколько вы получите в RUB' + '\n\n'
            text += f'<b>Лимиты:</b> от {round(LEFT_LIMIT/statement_db.get_xmr(), 6)} до {round(RIGHT_LIMIT/statement_db.get_xmr(), 6)} XMR'

        async with state.proxy() as file:
            file['buy'] = call.data

        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
        await FSMUser.input_quantity.set()


@dispatcher.message_handler(content_types=['text'], state=FSMUser.input_quantity)
async def add_shop(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        buy = file['buy']

    text: str = ''
    is_okay = False

    try:
        a = float(message.text)
        if 'btc' in buy:
            if a < round((LEFT_LIMIT / statement_db.get_btc()), 6):
                text += 'Введенное вами количество BTC ниже указанного лимита'
            elif a > round(RIGHT_LIMIT / statement_db.get_btc(), 6):
                text += 'Введенное вами количество BTC выше указанного лимита'
            else:
                is_okay = True
        elif 'eth' in buy:
            if a < round((LEFT_LIMIT / statement_db.get_eth()), 6):
                text += 'Введенное вами количество ETH ниже указанного лимита'
            elif a > round(RIGHT_LIMIT / statement_db.get_eth(), 6):
                text += 'Введенное вами количество ETH выше указанного лимита'
            else:
                is_okay = True
        elif 'ltc' in buy:
            if a < round((LEFT_LIMIT / statement_db.get_ltc()), 6):
                text += 'Введенное вами количество LTC ниже указанного лимита'
            elif a > round(RIGHT_LIMIT / statement_db.get_ltc(), 6):
                text += 'Введенное вами количество LTC выше указанного лимита'
            else:
                is_okay = True
        elif 'xmr' in buy:
            if a < round((LEFT_LIMIT / statement_db.get_xmr()), 6):
                text += 'Введенное вами количество XMR ниже указанного лимита'
            elif a > round(RIGHT_LIMIT / statement_db.get_xmr(), 6):
                text += 'Введенное вами количество XMR выше указанного лимита'
            else:
                is_okay = True
    except Exception as e:
        text = 'Введите данные в виде числа / дробного числа'
        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        print(e)

    if is_okay is True:
        async with state.proxy() as file:
            file['quantity'] = message.text

        if 'rub-' in buy:
            text = 'Выберите способ оплаты'
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_payment_type())
            await FSMUser.get_rub_payment.set()
        else:
            if '-rub' in buy:
                text = 'Укажите номер карты, на которую вам придут рубли'
                await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
                await FSMUser.get_reqs.set()
    else:
        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))


@dispatcher.message_handler(content_types=['text'], state=FSMUser.get_rub_payment)
async def get_rub_payment(message: types.Message, state: FSMContext):
    if message.text == 'Тинькофф':
        async with state.proxy() as file:
            file['rub_payment'] = 'tinkoff'
    elif message.text == 'Банк Открытие':
        async with state.proxy() as file:
            file['rub_payment'] = 'open_bank'
    elif message.text == 'Киви карта':
        async with state.proxy() as file:
            file['rub_payment'] = 'qiwi'

    async with state.proxy() as file:
        buy = file['buy']

    text = 'Введите адрес получения '

    if 'btc' in buy:
        text += 'BTC'
    elif 'eth' in buy:
        text += 'ETH'
    elif 'ltc' in buy:
        text += 'LTC'
    elif 'xmr' in buy:
        text += 'XMR'

    await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
    await FSMUser.get_reqs.set()


@dispatcher.message_handler(content_types=['text'], state=FSMUser.get_reqs)
async def get_crypto_address(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        file['reqs'] = message.text
        buy: str = file['buy']
        quantity = file['quantity']

    currency: str = ''

    text = '<i>📎Данные по сделке:</i>' + '\n\n'
    text += f'Операция: обмен <b>{buy.upper()}</b>' + '\n'
    if '-btc' in buy:
        async with state.proxy() as file:
            file['give'] = float(quantity) * statement_db.get_btc()
            file['get'] = float(quantity)
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_btc()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> BTC' + '\n'
        currency = 'BTC'
    elif '-eth' in buy:
        async with state.proxy() as file:
            file['give'] = float(quantity) * statement_db.get_eth()
            file['get'] = float(quantity)
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_eth()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> ETH' + '\n'
        currency = 'ETH'
    elif '-ltc' in buy:
        async with state.proxy() as file:
            file['give'] = float(quantity) * statement_db.get_ltc()
            file['get'] = float(quantity)
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_ltc()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> LTC' + '\n'
        currency = 'LTC'
    elif '-xmr' in buy:
        async with state.proxy() as file:
            file['give'] = float(quantity) * statement_db.get_xmr()
            file['get'] = float(quantity)
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_xmr()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> XMR' + '\n'
        currency = 'XMR'
    elif buy == 'btc-rub':
        async with state.proxy() as file:
            file['give'] = float(quantity)
            file['get'] = float(quantity) * statement_db.get_btc()
        text += f'Вы отдаете: <code>{float(quantity)}</code> BTC' + '\n'
        text += f'Вы получаете: <code>{float(quantity) * statement_db.get_btc()}</code> RUB' + '\n'
        currency = 'BTC'
    elif buy == 'ltc-rub':
        async with state.proxy() as file:
            file['give'] = float(quantity)
            file['get'] = float(quantity) * statement_db.get_ltc()
        text += f'Вы отдаете: <code>{float(quantity)}</code> LTC' + '\n'
        text += f'Вы получаете: <code>{float(quantity) * statement_db.get_ltc()}</code> RUB' + '\n'
        currency = 'LTC'
    elif buy == 'eth-rub':
        async with state.proxy() as file:
            file['give'] = float(quantity)
            file['get'] = float(quantity) * statement_db.get_eth()
        text += f'Вы отдаете: <code>{float(quantity)}</code> ETH' + '\n'
        text += f'Вы получаете: <code>{float(quantity) * statement_db.get_eth()}</code> RUB' + '\n'
        currency = 'ETH'
    elif buy == 'xmr-rub':
        async with state.proxy() as file:
            file['give'] = float(quantity)
            file['get'] = float(quantity) * statement_db.get_xmr()
        text += f'Вы отдаете: <code>{float(quantity)}</code> XMR' + '\n'
        text += f'Вы получаете: <code>{float(quantity) * statement_db.get_xmr()}</code> RUB' + '\n'
        currency = 'XMR'

    if 'rub-' in buy:
        text += f'Ваш адрес: <code>{message.text}</code>' + '\n\n'
    elif '-rub' in buy:
        text += f'Ваши реквизиты: <code>{message.text}</code>' + '\n\n'
    text += 'Все ли верно? Продолжаем ➡?'

    async with state.proxy() as file:
        file['currency'] = currency

    await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_is_correct(), parse_mode='HTML')
    await FSMUser.is_correct.set()


@dispatcher.message_handler(content_types=['text'], state=FSMUser.is_correct)
async def get_continued(message: types.Message, state: FSMContext):
    if message.text == 'Верно, продолжить':
        async with state.proxy() as file:
            buy = file['buy']
            currency = file['currency']
            give = file['give']
            get = file['get']

        text: str = ''

        if 'rub-' in buy:
            async with state.proxy() as file:
                rub_payment = file['rub_payment']

            text = f'На ваш кашелек будет зачислено <b>{get} {currency}</b>' + '\n\n'
            text += f'Отправьте <code>{give}</code> RUB' + '\n\n'
            text += '<b>Инструкция по оплате:</b>' + '\n'

            if rub_payment == 'tinkoff':
                text += f'Перевод на карту <code>{statement_db.get_tinkoff()}</code> (Тинькофф)' + '\n\n'
            elif rub_payment == 'open_bank':
                text += f'Перевод на карту <code>{statement_db.get_open_bank()}</code> (Банк Открытие)' + '\n\n'
            elif rub_payment == 'qiwi':
                text += f'Перевод на карту <code>{statement_db.get_qiwi()}</code> (Киви карта)' + '\n\n'
        elif '-rub' in buy:
            text += f'Вам на карту придет <b>{get}</b> RUB' + '\n'
            text += f'Отправьте <code>{give}</code> {currency}' + '\n\n'
            text += '<b>Инструкция по оплате:</b>' + '\n'

            if currency == 'BTC':
                text += f'Адрес: <code>{statement_db.get_btc_address()}</code> (BTC)' + '\n\n'
            elif currency == 'ETH':
                text += f'Адрес: <code>{statement_db.get_eth_address()}</code> (ETH)' + '\n\n'
            elif currency == 'LTC':
                text += f'Адрес: <code>{statement_db.get_ltc_address()}</code> (LTC)' + '\n\n'
            elif currency == 'XMR':
                text += f'Адрес: <code>{statement_db.get_xmr_address()}</code> (XMR)' + '\n\n'

        text += '<b>Внимание!</b> Tолько после оплаты нажмите на кнопку "Я оплатил(а)"'

        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_is_paid(), parse_mode='HTML')
        await FSMUser.is_paid.set()


@dispatcher.message_handler(content_types=['text'], state=FSMUser.is_paid)
async def is_paid(message: types.Message, state: FSMContext):
    if message.text == 'Я оплатил(а)':
        text = '🧾 Прикрепите изображение, подтверждающее оплату 📎⬇'
        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMUser.get_photo.set()


@dispatcher.message_handler(content_types=['photo'], state=FSMUser.get_photo)
async def get_photo(message: types.Message, state: FSMContext):
    numb = ''.join(random.choice(string.digits) for _ in range(random.randrange(8, 16)))

    async with state.proxy() as file:
        get = file['get']
        give = file['give']
        buy = file['buy']
        currency = file['currency']
        reqs = file['reqs']

    name = get_name(message)
    requests_db.add_request(request_id=numb, user_id=message.chat.id, name=name)

    for i in ADMIN_IDS:
        text = f'Номер заявки: <code>{numb}</code>' + '\n\n'
        if '-rub' in buy:
            text += f'Вам клиент отправил <b>{give} {currency}</b>' + '\n'
            text += f'Вы должны отправить <b>{get} RUB</b>' + '\n\n'
            text += f'Номер карты клиента: <code>{reqs}</code>' + '\n\n'
        elif 'rub-':
            text += f'Вам клиент отправил <b>{give} RUB</b>' + '\n'
            text += f'Вы должны отправить <b>{get} {currency}</b>' + '\n\n'
            text += f'Кошелек клиента: <code>{reqs}</code>' + '\n\n'

        text += f'Имя клиента: {str(name)}'

        try:
            await bot.send_photo(i, photo=message.photo[-1].file_id, caption=text, parse_mode='HTML', reply_markup=inline_markup_check_request())
        except Exception as e:
            print(e)

    text = f'Ваша заявка #<code>{numb}</code> сейчас находится на расмотрении 🔎' + '\n'
    text += '<i>Ожидайте, с вами скоро свяжутся...</i>'
    await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await clear_state(state)
    await send_menu(message)


@dispatcher.message_handler(state=FSMModeratorReply.request_id)
async def check_request_id(message: types.Message, state: FSMContext):
    if message.text == 'Главное меню':
        await bot.send_message(message.chat.id, 'Ок', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(message)
    else:
        if requests_db.request_exists(message.text):
            async with state.proxy() as file:
                file['request_id'] = message.text

            text = f'<code>{message.text}</code>\n\nЧто делаем с данной заявкой?'
            await bot.send_message(message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
            await FSMModeratorReply.choice.set()
        else:
            await bot.send_message(message.chat.id, 'Заявки с таким номером нет, введите еще раз', reply_markup=reply_markup_call_off('Главное меню'))
            await FSMModeratorReply.request_id.set()


@dispatcher.callback_query_handler(state=FSMModeratorReply.choice)
async def check_request_id(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'approve':
        text = 'Отправьте подтверждение оплаты'
        await bot.send_message(call.message.chat.id, text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMModeratorReply.blockchain.set()
    elif call.data == 'reject':
        async with state.proxy() as file:
            request_id = file['request_id']

        client_id = requests_db.get_user_id(request_id)
        text = f'<b>Заявка</b> #<code>{request_id}</code>' + '\n'
        text += 'Сделка прошла неуспешно, заявка отклонена ❌' + '\n\n'
        requests_db.delete_request(request_id)

        await bot.send_message(int(client_id), text=text, parse_mode='HTML')
        await bot.send_message(call.message.chat.id, 'Принято ✅', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(call.message)


@dispatcher.message_handler(content_types=['text'], state=FSMModeratorReply.blockchain)
async def check_request_id(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        request_id = file['request_id']

    if message.text == 'Отмена':
        await bot.send_message(chat_id=message.chat.id, text='Действие отменено', reply_markup=types.ReplyKeyboardRemove())
        text = f'<code>{request_id}</code>\n\nЧто делаем с данной заявкой?'
        await bot.send_message(message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
        await FSMModeratorReply.choice.set()
    else:
        client_id = requests_db.get_user_id(request_id)
        text = f'<b>Заявка</b> #<code>{request_id}</code>' + '\n'
        text += 'Сделка прошла успешно ✅' + '\n\n'
        text += message.text
        requests_db.delete_request(request_id)

        await bot.send_message(int(client_id), text=text, parse_mode='HTML')
        await bot.send_message(message.chat.id, 'Принято ✅', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(message)

try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)



