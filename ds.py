from google.cloud import datastore

def insert():
    client = datastore.Client('snapvite-app')

    kind = 'Task'
    name = 'sampletask1'
    task_key = client.key(kind, name)

    task = datastore.Entity(key=task_key)
    task['description'] = 'Buy milk'

    client.put(task)

def retrieve():
    client = datastore.Client('snapvite-app')
    entity = client.get(client.key('Task', 'sampletask1'))
    return entity