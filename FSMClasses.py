from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    buy = State()
    input_quantity = State()
    get_rub_payment = State()
    get_reqs = State()
    is_correct = State()
    is_paid = State()
    get_photo = State()
    calculator = State()
    get_amount = State()
    book_opps = State()
    review_input = State()


class FSMAdmin(StatesGroup):
    moderator_opps = State()
    moderator_input = State()


class FSMReply(StatesGroup):
    pass


class FSMModeratorReply(StatesGroup):
    request_id = State()
    choice = State()
    blockchain = State()

    review_id = State()
    review_opps = State()
