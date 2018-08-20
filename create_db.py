from sql_db import db
from sql_db import Tasks

db.create_all()
db.session.commit()