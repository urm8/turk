import asyncio
import re
import sys
from random import randrange

import aiohttp
from bs4 import BeautifulSoup
from database.sqlite_db import stats_table_read_stats, user_table_read_entries


def get_quiz_options(user_id: int):

    intermediate_crutch = user_table_read_entries(user_id)
    # [('üç', 'three'), ('orada', 'there'), ('bir', 'one'), ('iki', 'two')]

    correct_option_id = randrange(len(intermediate_crutch))
    new_word = intermediate_crutch[correct_option_id][0]
    new_question_options = []

    for option in intermediate_crutch:
        new_question_options.append(option[1])

    new_question = 'Choose correct translation for word ' + new_word + ':'

    # wrap in named tuple
    return new_word, new_question, correct_option_id, new_question_options


def get_quiz_stats(user_id: int):

    correct, incorrect = stats_table_read_stats(user_id)

    if (correct + incorrect) == 0:
        percentage = 0
    else:
        percentage = round(correct * 100 / (correct + incorrect), 2)

    return correct, incorrect, percentage  # wrap in named tuple


def normalize_word(phrase: str):

    processed_phrase = phrase.lower().translate(
        str.maketrans(
            '', '', '!\"#$%&\'()*+,./:;<=>?@[\]^_`{|}~1234567890',
        ),
    )

    pattern1 = re.compile(r'-{2,}')
    processed_phrase = pattern1.sub('-', processed_phrase)

    pattern2 = re.compile(r'[\n ]+')
    return '+'.join(pattern2.split(processed_phrase))


def parse_examples(text: str):

    examples = []
    soup = BeautifulSoup(text, 'lxml')
    table = soup.find('table', {'id': 'phrasetable'})

    if table:
        rows = table.find_all('tr')
    else:
        rows = []

    rows_count = len(rows)

    if rows_count >= 4:
        rows = rows[1:4]
    else:
        rows = rows[1:rows_count + 1]

    for row_number, row in enumerate(rows):
        cols = row.find_all('td')
        cols_count = len(cols)
        if cols_count >= 3:
            cols = cols[1:3]
        else:
            cols = []
        examples.append([])
        for element in cols:
            pure_element = element.text.strip()
            if pure_element:
                examples[row_number].append(pure_element)

    return examples


def normalize_examples(examples: list):

    intermediate_crutch = []

    for example in examples:
        intermediate_crutch.append(
            '\n\n_Translates as follows:_\n\n'.join(example),
        )

    return '' + '\n\n~ ~ ~ ~ ~ ~\n\n'.join(intermediate_crutch)


async def get_examples(word: str):

    url = 'https://www.multitran.com/m.exe?a=3&l1=32&l2=1&s=' + \
        normalize_word(word)
    examples = []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                status = resp.status
                if 200 <= status < 300:
                    answer = await resp.text()
                    examples = parse_examples(answer)
                else:
                    print(f'Server returned {status} status')
    except asyncio.TimeoutError:
        print('Timeout occurred', file=sys.stderr)
    except aiohttp.ClientError:
        print('ClientBase error occurred', file=sys.stderr)

    final_string = normalize_examples(examples)

    if final_string:
        return f'*Here are some examples with the word {word}:*\n\n' + final_string

    return f'Unfortunately can\'t find any examples with the word {word}.'
