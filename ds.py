from google.cloud import datastore

def insertSnapVite(username, message, recipients):
    client = datastore.Client('snapvite-app')

    kind = 'SnapVite'
    name = username + '001'
    snapvite_key = client.key(kind, name)

    snapvite = datastore.Entity(key=snapvite_key)
    snapvite['username'] = username
    snapvite['message'] = message
    snapvite['recipients'] = recipients

    client.put(snapvite)


def retrieve(snapvite_id):
    client = datastore.Client('snapvite-app')
    entity = client.get(client.key('SnapVite', snapvite_id))
    return str(entity)