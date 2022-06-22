from pydantic import BaseModel, Field


class Answer(BaseModel):
    content: str


class Poll(BaseModel):
    poll_id: int
    chat_id: int
    correct_option_id: int
    user_id: int


class WordIn(BaseModel):
    content: str
    lang_id: str


class WordOut(WordIn):
    id: int


class UserLanguageIn(BaseModel):
    native_language: str = Field(..., alias='native_language_id')
    learn_language: str = Field(..., alias='learn_language_id')


class UserLanguage(UserLanguageIn):
    user_id: int
