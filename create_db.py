from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
heroku_uri = 'postgres://ducsshdxzxljof:38f4754e47f7c3e5afec61085d1bbd08e03248d18d50640f80bcd32f3cd43c91@ec2-54-221-210-97.compute-1.amazonaws.com:5432/d9lss7ge2dbpr5'
app.config['SQLALCHEMY_DATABASE_URI'] = heroku_uri
db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))  
    done = db.Column(db.Boolean(200))

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

print('Started.......')
db.create_all()
db.session.commit()
task = Tasks('title','description',False)
db.session.add(task)
db.session.commit()
print('Completed......')