import requests  # pylint: disable=E0401
from requests.exceptions import RequestException  # pylint: disable=E0401
import os
import json
import re
from multiprocessing import Pool
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


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'rating': item[5]+item[6]
        }


def get_one_page(url):
    try:
        session_requests = requests.session()
        response = session_requests.get(url, headers=_get_headers())
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # multi process
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    # #single process
    # for i in range(10):
    # main(i*10)
