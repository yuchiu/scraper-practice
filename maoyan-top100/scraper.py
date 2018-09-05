import requests  # pylint: disable=E0401
from requests.exceptions import RequestException  # pylint: disable=E0401
import os
import random
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])

random.shuffle(USER_AGENTS)


def _get_headers():
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": ua
    }
    return headers


def get_one_page(url):
    try:
        session_requests = requests.session()
        response = session_requests.get(url, headers=_get_headers())
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def main():
    url = 'http://maoyan.com/board'
    html = get_one_page(url)
    print(html)


if __name__ == '__main__':
    main()
