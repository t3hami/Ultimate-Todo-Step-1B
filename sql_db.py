from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
heroku_uri = ''
local_uri = 'sqlite:///todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ducsshdxzxljof:38f4754e47f7c3e5afec61085d1bbd08e03248d18d50640f80bcd32f3cd43c91@ec2-54-221-210-97.compute-1.amazonaws.com:5432/d9lss7ge2dbpr5'
db = SQLAlchemy(app)

class SQL:

    def __init__(self, app=app):
        local_uri = 'sqlite:///todo.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ducsshdxzxljof:38f4754e47f7c3e5afec61085d1bbd08e03248d18d50640f80bcd32f3cd43c91@ec2-54-221-210-97.compute-1.amazonaws.com:5432/d9lss7ge2dbpr5'
        db = SQLAlchemy(app)

    def get_all_tasks(self):
        data = Tasks.query.all()
        tasks = []
        for task in data:
            tasks.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done
                })
        return tasks

    def post_task(self, task):
        task = Tasks(task['title'],task['description'],task['done'])
        db.session.add(task)
        db.session.commit()
        return task.id
    
    def is_task_present(self, id):
        is_task = Tasks.query.filter_by(id=id).first()
        if is_task:
            return True
        return False

    def get_task(self, id):
        data = Tasks.query.filter_by(id=id).first()
        return {
            '_id': data.id,
            'title': data.title,
            'description': data.description,
            'done': data.done
        }

    def delete_task(self, id):
        delete_data = Tasks.query.filter_by(id=id).first()
        db.session.delete(delete_data)
        db.session.commit()

    def update_task(self, id, task):
        update_data = Tasks.query.filter_by(id=id).first()
        update_data.title = task['title']
        update_data.description = task['description']
        update_data.done = task['done']
        db.session.commit()



class Tasks(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))  
    done = db.Column(db.Boolean(200))

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done
