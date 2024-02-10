import json

secrets_store = {}

# Load up private data
def get_secrets():
    global secrets_store

    with open('src/secrets.json', 'r') as openfile:
        secrets_store = json.load(openfile)
