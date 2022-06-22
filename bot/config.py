from os import environ

from dotenv import load_dotenv
from furl import furl

load_dotenv()

TOKEN = environ['SECRET']  # really, just put it in
API_URL = furl(environ['API_URL']) / 'api'
API_KEY = environ['API_KEY']
