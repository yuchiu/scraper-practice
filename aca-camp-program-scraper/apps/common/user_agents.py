import os
import sys
import random


""" setup user agent """
USER_AGENTS_FILE = os.path.join(
    os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])

random.shuffle(USER_AGENTS)


def get_headers():
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": ua
    }
    return headers
