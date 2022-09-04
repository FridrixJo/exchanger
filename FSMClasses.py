from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    buy = State()
    input_quantity = State()
    get_rub_payment = State()
    get_reqs = State()
    get_crypto_address = State()
    is_correct = State()
    is_paid = State()


class FSMAdmin(StatesGroup):
    moderator_opps = State()
    active = State()


class FSMReply(StatesGroup):
    pass
