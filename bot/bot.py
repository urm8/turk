import logging
import traceback
from http.client import HTTPException

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import PollAnswer, ReplyKeyboardRemove
from aiogram.utils import executor
from auxiliary_logic.quiz_supply import (
    get_examples,
    get_quiz_options,
    get_quiz_stats,
)
from client import PollsAnswerClient, UserLanguageClient, WordsClient
from config import TOKEN
from database import redis
from database.sqlite_db import (
    answer_table_delete_entry,
    sql_start,
    stats_table_check_entry_existence,
    stats_table_create_entry,
    user_table_add_default_entries,
    user_table_add_entry,
    user_table_check_entry_existence,
    user_table_check_existence,
    user_table_create,
    user_table_delete_entry,
)
from fsm import FSMAdd, FSMRemove, FSMSetLanguage
from keyboards import main_kb, quiz_kb, restart_kb, yn_kb

# log level

logging.basicConfig(level=logging.INFO)

# adding storage for finite-state machine
fsm_storage = MemoryStorage()
storage = RedisStorage2(
    'localhost', 6379, db=0,
    pool_size=10, prefix='turk-bot',
)

# bot initialization
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# adding finite-state machines and their states


# console message on startup
async def on_startup(_):
    print('Bot is online')
    sql_start()


# start chatting
@dp.message_handler(commands=['start', 'help'], state='*')
async def conversation_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()

    if not stats_table_check_entry_existence(message.chat.id):
        stats_table_create_entry(message.chat.id)

    user_table_create(message.chat.id)
    user_table_add_default_entries(message.chat.id)
    answer_table_delete_entry(message.chat.id)

    await message.answer(
        '*Welcome to the mdncv_bot_v2.0!*\n\n'
        'This bot will help you learn new Turkish words in a quiz format.\n'
        'Just add a few words along with the description, start the quiz and have fun!',
        reply_markup=main_kb, parse_mode='Markdown',
    )


# return to menu
@dp.message_handler(state='*', commands=['menu', 'cancel', 'finish', 'stop'])
@dp.message_handler(Text(equals=['cancel', 'finish', 'stop'], ignore_case=True), state='*')
async def go_to_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    answer_table_delete_entry(message.chat.id)

    await message.answer('Returning to main menu..', reply_markup=main_kb)


# quiz start
@dp.message_handler(commands=['quiz'])
async def quiz_start(message: types.Message):
    new_word, new_question, correct_option_id, new_question_options = get_quiz_options(
        message.chat.id,
    )
    current_poll = await bot.send_poll(
        message.chat.id,
        question=new_question,
        options=new_question_options,
        is_anonymous=False,
        type='quiz',
        correct_option_id=correct_option_id,
        reply_markup=quiz_kb,
    )
    poll = current_poll.poll
    await dp.storage.set_data(user=message.from_user.id, data={'correct_option_id': poll.correct_option_id})


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: PollAnswer):
    data = await dp.storage.get_data(user=quiz_answer.user.id)
    correct_option_id = data.pop('correct_option_id')
    cheers_client = PollsAnswerClient()
    if correct_option_id in quiz_answer.option_ids:
        cheer = await cheers_client.get_cheer_positive(quiz_answer.user.language_code)
        if cheer:
            await bot.send_message(quiz_answer.user.id, cheer.content)
    else:
        cheer = await cheers_client.get_cheer_negative(quiz_answer.user.language_code)
        if cheer:
            await bot.send_message(quiz_answer.user.id, cheer.content)
        examples = await get_examples(current_word)
        await bot.send_message(quiz_answer.user.id, examples, parse_mode='Markdown')


@dp.message_handler(commands=['stats'])
async def stats_track(message: types.Message):
    answer_table_delete_entry(message.chat.id)

    if stats_table_check_entry_existence(message.chat.id):
        correct, incorrect, percentage = get_quiz_stats(message.chat.id)
        await message.answer(
            f'Correct answers count: {correct}\nIncorrect answers count: {incorrect}\n'
            f'Total answers count: {correct + incorrect}\n\n'
            f'Current correct answer percentage: {percentage}%',
            reply_markup=quiz_kb,
        )
    else:
        await message.answer('Please restart the bot, some trouble happened.', reply_markup=restart_kb)


# adding word section
@dp.message_handler(commands=['add'], State=None)
async def add_word(message: types.Message):
    if user_table_check_existence(message.chat.id):
        await FSMAdd.addition_word.set()
        await message.answer('What word do you want to add?', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Please restart the bot, some trouble happened.', reply_markup=restart_kb)


@dp.message_handler(state=FSMAdd.addition_word)
async def get_word_to_add(message: types.Message, state: FSMContext):
    async with state.proxy() as word:
        word['addition_word'] = message.text
    await FSMAdd.next()
    await message.answer(f'What is the \"{message.text}\" word\'s translation in your native language ?')


class BotException(Exception):
    pass


class LanguageNotSetException(BotException):
    pass


async def get_user_lang_conf(user_id, source_target) -> tuple[str, str]:
    key = f'bot-lang-{user_id}'
    if value := await redis.get(key):
        return value
    else:
        try:
            lang = await UserLanguageClient().get_user_language(user_id)
        except HTTPException:
            await FSMSetLanguage.start()
            raise LanguageNotSetException()

        source_target = (lang.native_language, lang.learn_language)
        await redis.set(key, source_target)
        return source_target


@dp.message_handler(state=FSMAdd.addition_word_description)
async def get_added_words_description(message: types.Message, state: FSMContext):
    user_id = await get_user_lang_conf(message.from_user.id)
    try:
        native, target = await get_user_lang_conf(user_id)
    except LanguageNotSetException:
        await state.finish()
        return

    async with state.proxy() as word:
        the_word = await WordsClient.add_word(word['addition_word'])
        the_translation = await TranslationClient
        await message.answer(
            f'Word \"{word["addition_word"]}\" added.', reply_markup=quiz_kb,
        )

    await state.finish()


@dp.message_handler(commands=['lang'], State=None)
async def set_language(message: types.Message) -> None:
    """/lang sets current user language."""
    await FSMSetLanguage.start.set()
    await message.answer('What is your mother tongue?', reply_markup=ReplyKeyboardRemove())
    await FSMSetLanguage.next()


@dp.message_handler(state=FSMSetLanguage.source_lang)
async def set_source_lang(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['source_lang'] = message.text
    await FSMSetLanguage.next()
    await message.answer('What language are you trying to learn?')


@dp.message_handler(state=FSMSetLanguage.target_lang)
async def set_target_lang(message: types.Message, state: FSMContext) -> None:
    client = UserLanguageClient()
    source_lang = message.from_user.language_code
    async with state.proxy() as proxy:
        source_lang = proxy.get('source_lang', source_lang)
    target_language = message.text
    await message.answer(f'I assume that your mother tongue is "{source_lang}" and you are trying to learn "{target_language}"')
    try:
        ans = await client.set_user_language(message.from_user.id, source_lang, target_language)
        await message.answer(f'Successfully set you up with: {ans.native_language} => {ans.learn_language}')
    except Exception as e:
        await message.answer(f'Damn, something bad happened: {e}. The traceback is: {traceback.format_exc()}')
    await state.finish()


# remove word section
@dp.message_handler(commands=['remove'], state=None)
async def remove_word(message: types.Message):
    if user_table_check_existence(message.chat.id):
        await FSMRemove.remove_word.set()
        answer_table_delete_entry(message.chat.id)
        await message.answer('What word do you want to remove?', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Please restart the bot, some trouble happened.', reply_markup=restart_kb)


@dp.message_handler(state=FSMRemove.remove_word)
async def get_word_to_remove(message: types.Message, state: FSMContext):
    async with state.proxy() as word:
        word['remove_word'] = message.text

    if user_table_check_entry_existence(message.text, message.chat.id):
        await FSMRemove.next()
        await message.answer(
            f'The word \"{message.text}\" will be removed, are you sure?',
            reply_markup=yn_kb,
        )
    else:
        await message.answer(f'The word \"{message.text}\" is not in dictionary.', reply_markup=quiz_kb)
        await state.finish()


@dp.message_handler(state=FSMRemove.remove_word_yn, commands=['yes'])
async def remove_word_y(message: types.Message, state: FSMContext):
    async with state.proxy() as word:
        user_table_delete_entry(word['remove_word'], message.chat.id)
        await message.answer(
            f'The word \"{word["remove_word"]}\" had been removed.', reply_markup=quiz_kb,
        )
    await state.finish()


@dp.message_handler(state=FSMRemove.remove_word_yn, commands=['no'])
async def remove_word_n(message: types.Message, state: FSMContext):
    async with state.proxy() as word:
        await message.answer(
            f'The word \"{word["remove_word"]}\" had not been removed.', reply_markup=quiz_kb,
        )

    await state.finish()


# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
