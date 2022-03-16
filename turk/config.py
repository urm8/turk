import os
import peewee

db = peewee.SqliteDatabase('words.db')
api_key = os.environ['KEY']