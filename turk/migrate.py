from turk.config import db
from turk.models import Word, Translation

db.drop_tables([Translation, Word])
db.create_tables([Word, Translation], safe=True)