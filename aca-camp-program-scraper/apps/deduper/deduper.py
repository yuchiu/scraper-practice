
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient   # pylint: disable=E0401
import json
from os.path import join, dirname
from dotenv import load_dotenv  # pylint: disable=E0401
import mongodb_client  # pylint: disable=E0401

dotenv_path = join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

MQ_CAMP_DEDUPER_TASK_NAME = os.environ.get("MQ_CAMP_DEDUPER_TASK_NAME")
MQ_CAMP_DEDUPER_TASK_URI = os.environ.get("MQ_CAMP_DEDUPER_TASK_URI")


dedupe_camp_client = CloudAMQPClient(
    MQ_CAMP_DEDUPER_TASK_URI, MQ_CAMP_DEDUPER_TASK_NAME)

SLEEP_TIME_IN_SECONDS = 1

CAMP_DB_MONGO_TABLE = os.environ.get("CAMP_DB_MONGO_TABLE")


def handle_message(msg):
    task = json.loads(msg)
    # update database
    db = mongodb_client.get_db()
    db[CAMP_DB_MONGO_TABLE].replace_one(
        {'camp_id': task['camp_id']}, task, upsert=True)


def run():
    while True:
        if dedupe_camp_client is not None:
            msg = dedupe_camp_client.getMessage()
            if msg is not None:
                # Parse and process the task
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass

            dedupe_camp_client.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == '__main__':
    run()
