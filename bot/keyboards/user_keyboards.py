from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

quiz_btn = KeyboardButton('/quiz')
add_btn = KeyboardButton('/add')
rm_btn = KeyboardButton('/remove')
stats_btn = KeyboardButton('/stats')
menu_btn = KeyboardButton('/menu')
lang_btn = KeyboardButton('/lang')

yes_btn = KeyboardButton('/yes')
no_btn = KeyboardButton('/no')

again_btn = InlineKeyboardButton('again')

start_btn = KeyboardButton('/start')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
quiz_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yn_kb = ReplyKeyboardMarkup(resize_keyboard=True)
restart_kb = ReplyKeyboardMarkup(resize_keyboard=True)
poll_kb = ReplyKeyboardMarkup(resize_keyboard=None)
quiz_ikb = InlineKeyboardMarkup(row_width=1)

main_kb.add(quiz_btn).insert(stats_btn).add(
    add_btn,
).insert(rm_btn).insert(lang_btn)
quiz_kb.add(quiz_btn).add(stats_btn).add(menu_btn)
quiz_ikb.add(again_btn)
yn_kb.add(yes_btn).insert(no_btn)
restart_kb.add(start_btn)
