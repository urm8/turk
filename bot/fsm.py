from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdd(StatesGroup):
    addition_word = State()
    addition_word_description = State()


class FSMRemove(StatesGroup):
    remove_word = State()
    remove_word_yn = State()


class FSMSetLanguage(StatesGroup):
    start = State()
    source_lang = State()
    target_lang = State()
