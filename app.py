from flask import Flask, request, jsonify
from sql_db import SQL

app = Flask(__name__)

postgre = SQL(app)


@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        all_tasks = postgre.get_all_tasks()
        return jsonify(all_tasks)

    elif request.method == 'POST':
        try:
            task = {
                'title': request.json['title'],
                'description': request.json['description'],
                'done': False
            }
            id = postgre.post_task(task)
            return jsonify({'status': 'Success', '_id': str(id)})
        except KeyError:
            return jsonify({'status': 'Missing title or discription, or both.'})


@app.route('/todo/api/v1.0/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    if request.method == 'GET':
        if postgre.is_task_present(task_id):
            task = postgre.get_task(task_id)
            return jsonify(task)
        else:
            return jsonify({'status': 'There is no task with _id: ' + task_id})

    elif request.method == 'PUT':
        if postgre.is_task_present(task_id):
            if not request.json or not isinstance(request.json['done'],bool):
                return jsonify({'status': 'Please provide atleast one key, value to update. (done key must be boolean)'})
            old_task = {}
            old_task = postgre.get_task(task_id)
            old_task['_id'] = int(old_task['_id'])
            updated_task = {}
            for key in old_task.keys():
                try:
                    updated_task[key] = request.json[key]
                except:
                    updated_task[key] = old_task[key]
            postgre.update_task(task_id, updated_task)
            return jsonify({'status': 'Success'})
        else:
            return jsonify({'status': 'There is no task with _id: ' + task_id})

    elif request.method == 'DELETE':
        if postgre.is_task_present(task_id):
            postgre.delete_task(task_id)
            return jsonify({'status': 'Success'})
        else:
            return jsonify({'status': 'There is no task with _id: ' + task_id})
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)