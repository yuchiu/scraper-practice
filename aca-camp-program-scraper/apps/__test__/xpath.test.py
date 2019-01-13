import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import user_agents  # pylint: disable=E0401
import requests  # pylint: disable=E0401
import random
import json
import time
from lxml import html
import re


SLEEP_TIME_IN_SECONDS = 1
# 2256
TEST_URL = "http://find.acacamps.org/program_profile.php?back=camp_profile&program_id=3000"

TEST_XPATH = '''//*[@id="fac-program-profile"]/section[5]/div/div/div/div/ul/li/text()'''


def run():
    session_requests = requests.session()
    response = session_requests.get(
        TEST_URL, headers=user_agents.get_headers())
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        test = tree.xpath(TEST_XPATH)

        if(len(test) > 0):
            test = test
        else:
            test = ''

        print('test')
        print(test)


if __name__ == '__main__':
    run()
