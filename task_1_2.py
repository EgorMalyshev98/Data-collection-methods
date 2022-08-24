import requests
from pprint import pprint


def get_groups(token: str) -> list:
    url = f'https://api.vk.com/method/groups.get?v=5.131&access_token={token}'

    res = requests.get(url).json()

    return res.get('response').get('items')


access_token = 'your token'

pprint(get_groups(access_token))
