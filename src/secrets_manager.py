import json

# Load up private data
def get_secrets():

    with open('src/secrets.json', 'r') as openfile:
        secrets_store = json.load(openfile)

        return secrets_store
