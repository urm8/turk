from ninja import NinjaAPI
from words.api import R as words_api

api = NinjaAPI(title='turk-api')
api.add_router('words', words_api)
