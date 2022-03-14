from turk.config import db
from turk.models import Word, Translation

db.create_tables([Word, Translation], safe=True)