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


storage = MemoryStorage()

bot = Bot(TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(ADMIN_ID)]


users_db = UsersDB('data_base/exchanger.db')
statement_db = StatementDB('data_base/exchanger.db')


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


@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMUser.input_quantity, FSMUser.get_crypto_address, FSMUser.get_rub_payment, FSMUser.is_correct])
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
        pass
    elif call.data == 'about':
        pass
    elif call.data == 'calculator':
        pass
    elif call.data == 'review':
        pass
    elif call.data == 'how':
        pass


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
            if 'btc-' in buy:
                pass
            elif 'eth-' in buy:
                pass
            elif 'ltc-' in buy:
                pass
            elif 'xmr-' in buy:
                pass
    else:
        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))


@dispatcher.message_handler(state=FSMUser.get_rub_payment)
async def get_rub_payment(message: types.Message, state: FSMContext):
    if message.text == 'Сбербанк RUB':
        async with state.proxy() as file:
            file['rub_payment'] = 'sber'
    elif message.text == 'Тинькофф RUB':
        async with state.proxy() as file:
            file['rub_payment'] = 'tinkoff'

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
    await FSMUser.get_crypto_address.set()


@dispatcher.message_handler(state=FSMUser.get_crypto_address)
async def get_crypto_address(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        file['address'] = message.text
        buy: str = file['buy']
        quantity = file['quantity']

    currency: str  = ''

    text = '<i>📎Данные по сделке:</i>' + '\n\n'
    text += f'Операция: обмен <b>{buy.upper()}</b>' + '\n'
    if '-btc' in buy:
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_btc()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> BTC' + '\n'
        currency = 'BTC'
    elif '-eth' in buy:
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_eth()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> ETH' + '\n'
        currency = 'ETH'
    elif '-ltc' in buy:
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_ltc()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> LTC' + '\n'
        currency = 'LTC'
    elif '-xmr' in buy:
        text += f'Вы отдаете: <code>{float(quantity) * statement_db.get_xmr()}</code> RUB' + '\n'
        text += f'Вы получаете: <code>{float(quantity)}</code> XMR' + '\n'
        currency = 'XMR'

    text += f'Ваш адрес: {message.text}' + '\n\n'
    text += 'Все ли верно? Продолжаем ➡?'

    async with state.proxy() as file:
        file['currency'] = currency

    await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_is_correct(), parse_mode='HTML')
    await FSMUser.is_correct.set()


@dispatcher.message_handler(state=FSMUser.is_correct)
async def get_continued(message: types.Message, state: FSMContext):
    if message.text == 'Верно, продолжить':
        async with state.proxy() as file:
            currency = file['currency']
            quantity = file['quantity']
            rub_payment = file['rub_payment']

        text = f'На ваш кашелек будет зачислено <b>{quantity} {currency}</b>' + '\n\n'
        if currency == 'BTC':
            text += f'Отправьте <code>{float(quantity) * statement_db.get_btc()}</code> RUB' + '\n\n'
        elif currency == 'ETH':
            text += f'Отправьте <code>{float(quantity) * statement_db.get_eth()}</code> RUB' + '\n\n'
        elif currency == 'LTC':
            text += f'Отправьте <code>{float(quantity) * statement_db.get_ltc()}</code> RUB' + '\n\n'
        elif currency == 'XMR':
            text += f'Отправьте <code>{float(quantity) * statement_db.get_xmr()}</code> RUB' + '\n\n'

        text += '<b>Инструкция по оплате:</b>' + '\n'
        if rub_payment == 'sber':
            text += f'Перевод на карту <code>{statement_db.get_sber()}</code> (Сбербанк)' + '\n\n'
        elif rub_payment == 'tinkoff':
            text += f'Перевод на карту <code>{statement_db.get_tinkoff()}</code> (Тинькофф)' + '\n\n'

        text += '<b>Внимание!</b> Tолько после оплаты нажмите на кнопку "Я оплатил(а)"'

        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_is_paid(), parse_mode='HTML')
        await FSMUser.is_paid.set()






try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)



