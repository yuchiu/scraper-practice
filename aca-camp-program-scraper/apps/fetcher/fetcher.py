# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import user_agents  # pylint: disable=E0401
import requests  # pylint: disable=E0401
import time
from cloudAMQP_client import CloudAMQPClient  # pylint: disable=E0401
from dotenv import load_dotenv  # pylint: disable=E0401
from lxml import html
from parse_camp import parse_camp_details  # pylint: disable=E0401
from parse_program import parse_program_details  # pylint: disable=E0401

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

MQ_CAMP_FETCHER_TASK_NAME = os.environ.get("MQ_CAMP_FETCHER_TASK_NAME")
MQ_CAMP_FETCHER_TASK_URI = os.environ.get("MQ_CAMP_FETCHER_TASK_URI")

MQ_CAMP_DEDUPER_TASK_NAME = os.environ.get("MQ_CAMP_DEDUPER_TASK_NAME")
MQ_CAMP_DEDUPER_TASK_URI = os.environ.get("MQ_CAMP_DEDUPER_TASK_URI")

SLEEP_TIME_IN_SECONDS = 1

fetch_camp_client = CloudAMQPClient(
    MQ_CAMP_FETCHER_TASK_URI, MQ_CAMP_FETCHER_TASK_NAME)
dedupe_camp_client = CloudAMQPClient(
    MQ_CAMP_DEDUPER_TASK_URI, MQ_CAMP_DEDUPER_TASK_NAME)


def spider(request_url):
    session_requests = requests.session()
    response = session_requests.get(
        request_url, headers=user_agents.get_headers())
    try:
        tree = html.fromstring(response.content)
    except Exception:
        print('request camp page failed')
        return {}

    return tree


def handle_message(msg):
    task = json.loads(msg)
    url = task['url']
    camp_id = task['camp_id']

    # get individual camp details
    camp_dom_tree = spider(url)
    task_data = parse_camp_details(camp_dom_tree)
    task_data['camp_id'] = camp_id

    # loop program_url_list and get individual program details
    program_url_list = task_data['program_url_list']
    program_list = []
    if len(program_url_list) > 0:
        for program_url in program_url_list:
            program_dom_tree = spider(program_url)
            program_data = parse_program_details(program_dom_tree)
            program_data['camp_id'] = camp_id
            program_list.append(program_data)
            time.sleep(SLEEP_TIME_IN_SECONDS)

    # save program list to task_data
    task_data['program_list'] = program_list
    dedupe_camp_client.sendMessage(task_data)


def run():
    while True:
        if fetch_camp_client is not None:
            msg = fetch_camp_client.getMessage()
            if msg is not None:
                # parse and process the task
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            fetch_camp_client.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == "__main__":
    run()
