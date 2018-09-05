try:
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlencode  # pylint: disable=E0401
import requests  # pylint: disable=E0401
from requests.exceptions import RequestException  # pylint: disable=E0401
import json
import re


def get_page_index(offset, keyword):
    data = {
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": 20,
        "cur_tab": 1,
        "from": "search_tab"
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('request index failed')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def main():
    html = get_page_index(0, "autoshow")
    for url in parse_page_index(html):
        print(url)


if __name__ == '__main__':
    main()
