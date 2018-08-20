import unittest
import app
import requests
import json


class TestApp(unittest.TestCase):

    def test_get_all_tasks(self):
        response = requests.get('http://127.0.0.1:5000/todo/api/v1.0/tasks')
        # Checking response status
        self.assertEqual(response.status_code, 200)
        # Checking returned data type
        self.assertEqual(isinstance(response.json(),list), True)

    def test_post_task_complete(self):
        # Data for post request (Complete)
        data = {
            'title': 'Unit testing',
            'description': 'This is for unit testing......',
            'done': True
        }
        response = requests.post('http://127.0.0.1:5000/todo/api/v1.0/tasks', json.dumps(data), headers={'content-type': 'application/json'})
        # Checking response status
        self.assertEqual(response.status_code, 200)
        # Checking response text that I have set when data is complete
        self.assertEqual(response.json()['status'], 'Success')

    def test_post_task_incomplete(self):
        # Data for post request (Incomplete)
        data = {
            #'title': 'Unit testing',
            'description': 'This is for unit testing......',
            'done': True
        }
        response = requests.post('http://127.0.0.1:5000/todo/api/v1.0/tasks', json.dumps(data), headers={'content-type': 'application/json'})
        # Checking response status
        self.assertEqual(response.status_code, 200)
        # Checking response text that I have set when data is incomplete
        self.assertEqual(response.json()['status'], 'Missing title or discription, or both.')

    def test_validate_id(self):
        # Request with wrong id
        wrong_id = 'abcdcdcjdvjfvfmf'
        response = requests.get('http://127.0.0.1:5000/todo/api/v1.0/tasks/'+wrong_id)
        self.assertEqual(response.status_code, 200)
        # Checking status for wrong id
        self.assertEqual(response.json()['status'],'There is no task with _id: '+wrong_id)
    
    def test_edit_task(self):
        # I will post a task and then update it
        data = {
            'title': 'Before update',
            'description': 'I will be updated.',
            'done': False
        }
        response = requests.post('http://127.0.0.1:5000/todo/api/v1.0/tasks', json.dumps(data), headers={'content-type': 'application/json'})
        # Get id of posted data
        id = response.json()['_id']

        # Now edit data of previous id
        data = {
            'title': 'After update',
            'description': 'I was updated in unit test.',
            'done': True
        }
        response = requests.put('http://127.0.0.1:5000/todo/api/v1.0/tasks/'+id, json.dumps(data), headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 200)

        # Edit again with no data
        response = requests.put('http://127.0.0.1:5000/todo/api/v1.0/tasks/'+str(id),json.dumps({}), headers={'content-type': 'application/json'})
        # Checking response when no data is provided
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'],'Please provide atleast one key, value to update')
    
    def test_delete_task(self):
        # I will post a task and then delete it
        data = {
            'title': 'I will be deleted',
            'description': 'Good bye.',
            'done': False
        }
        response = requests.post('http://127.0.0.1:5000/todo/api/v1.0/tasks', json.dumps(data), headers={'content-type': 'application/json'})
        # Get id of posted data
        id = response.json()['_id']

        # Delete data previously created
        response = requests.delete('http://127.0.0.1:5000/todo/api/v1.0/tasks/'+str(id))
        # Checking response status code
        self.assertEqual(response.status_code, 200)
        # Checking response status text
        self.assertEqual(response.json()['status'], 'Success')

def clear_collection():
    response = requests.get('http://127.0.0.1:5000/todo/api/v1.0/tasks')
    for r in response.json():
        response = requests.delete('http://127.0.0.1:5000/todo/api/v1.0/tasks/'+str(r['id']))


if __name__ == '__main__':
    clear_collection()  # Clear all the old data
    unittest.main()