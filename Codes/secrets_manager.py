import json

secrets_store = {}

def get_secrets():
    global secrets_store

    with open('secrets.json', 'r') as openfile:
        secrets_store = json.load(openfile)
