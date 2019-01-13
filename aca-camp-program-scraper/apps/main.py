import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
import time
from cloudAMQP_client import CloudAMQPClient  # pylint: disable=E0401
from dotenv import load_dotenv  # pylint: disable=E0401

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

MQ_CAMP_FETCHER_TASK_NAME = os.environ.get("MQ_CAMP_FETCHER_TASK_NAME")
MQ_CAMP_FETCHER_TASK_URI = os.environ.get("MQ_CAMP_FETCHER_TASK_URI")

fetch_camp_client = CloudAMQPClient(
    MQ_CAMP_FETCHER_TASK_URI, MQ_CAMP_FETCHER_TASK_NAME)

SLEEP_TIME_IN_SECONDS = 1

ROOT_URL = "http://find.acacamps.org/camp_profile.php?camp_id="


def build_camp_url(index):
    camp_url = '%s%s' % (ROOT_URL, str(index))
    return camp_url


def run():
    ''' loop camps url list from a index page and fetch each individual camp's URL as task to Message Queue '''
    for index in range(1, 4869):
        camp_url = build_camp_url(index)
        task = {'url': camp_url, 'camp_id': index}
        fetch_camp_client.sendMessage(task)
        time.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == '__main__':
    run()
