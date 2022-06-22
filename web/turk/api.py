from ninja import NinjaAPI
from ninja.security import HttpBearer
from polls.api import polls_api
from words.api import words_router


class AuthBearer(HttpBearer):
    def authenticate(self, request, token) -> bool:
        return self.get_token(request, token)

    @staticmethod
    def get_token(*args, **kwargs) -> bool:
        return True


api = NinjaAPI(title='turk-api')

api.add_router('words', words_router)
api.add_router('polls', polls_api, auth=AuthBearer())
