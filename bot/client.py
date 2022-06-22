from __future__ import annotations

from contextlib import suppress
from typing import Generic, TypeVar

import aiohttp
from aiohttp.web_exceptions import HTTPException
from config import API_KEY, API_URL
from furl import furl
from pydantic import BaseModel
from response_schema import Answer, Poll, UserLanguage, WordOut

R = TypeVar('R', bound=BaseModel)


class ClientBase(Generic[R]):
    def __init__(self, model: type[R], base_url: furl, auth: str) -> None:
        self.model = model
        self._base_url = base_url
        self._auth = auth

    async def close(self) -> None:
        return await self._client.close()

    async def __aenter__(self) -> "ClientBase":
        return self

    async def __aexit__(self, *args, **kwargs) -> bool | None:
        await self.close()
        return None

    def _make_url(self, path: str) -> str:
        return (self._base_url / path).url

    async def _make_request(self, method: str, path: str, *args, **kwargs) -> dict:
        headers = kwargs.pop('headers', {})
        headers.update({'Authorization': f'Bearer {self._auth}'})
        async with aiohttp.ClientSession(raise_for_status=False) as client,\
                getattr(client, method)(self._make_url(path), *args, headers=headers, **kwargs) as response:
            r = await response.json()
            return r

    async def get(self, path: str, *args, **kwargs) -> R:
        value = await self._make_request('get', path, *args, **kwargs)
        return self.model.parse_obj(value)

    async def post(self, path: str, *args, **kwargs) -> R:
        value = await self._make_request('post', path, *args, **kwargs)
        return self.model.parse_obj(value)

    async def delete(self, path: str, *args, **kwargs) -> None:
        await self._make_request('delete', path, *args, **kwargs)

    async def patch(self, path: str, *args, **kwargs) -> R:
        value = await self._make_request('patch', path, *args, **kwargs)
        return self.model.parse_obj(value)


class LanguageClient(ClientBase):
    pass


class PollsAnswerClient(ClientBase[Answer]):

    def __init__(self) -> None:
        super().__init__(Answer, API_URL / 'polls', API_KEY)

    async def get_cheer_positive(self, lang: str) -> Answer:
        with suppress(HTTPException):
            return await self.get(f'/answer/{lang}/correct/')

    async def get_cheer_negative(self, lang: str) -> Answer:
        with suppress(HTTPException):
            return await self.get(f'/answer/{lang}/incorrect/')


class PollsPollClient(ClientBase[Poll]):

    def __init__(self) -> None:
        super().__init__(Poll, API_URL / 'api' / 'polls', API_KEY)

    async def add_poll(self, poll_id, chat_id, user_id, correct_option_id) -> Poll:
        payload = {
            'poll_id': poll_id,
            'chat_id': chat_id,
            'correct_option_id': correct_option_id,
        }
        return await self.post(
            f'/{user_id}/poll/', json=payload,
        )

    async def get_poll(self, poll_id, user_id) -> Poll:
        return await self.get(f'/{user_id}/{poll_id}/')


class WordsClient(ClientBase[WordOut]):

    def __init__(self, model: type[R], base_url: furl, auth: str) -> None:
        super().__init__(WordOut, API_URL / 'words', API_KEY)

    async def add_word(self, content, lang):
        pass

    async def search_word(self, content, lang):
        pass

    async def get_examples(self, content, lang):
        pass


class UserLanguageClient(ClientBase[UserLanguage]):
    def __init__(self) -> None:
        super().__init__(UserLanguage, API_URL / 'polls', API_KEY)

    async def set_user_language(self, user_id: int, local_language: str, target_language: str) -> UserLanguage:
        payload = {
            'native_language': local_language,
            'learn_language': target_language,
        }
        return await self.post(f'{user_id}/language/', json=payload)

    async def get_user_language(self, user_id: int) -> UserLanguage:
        return await self.get(f'{user_id}/language/')


class TranslationClient(ClientBase[])
