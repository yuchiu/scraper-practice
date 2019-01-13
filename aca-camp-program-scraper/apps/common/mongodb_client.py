from pymongo import MongoClient  # pylint: disable=E0401
import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv  # pylint: disable=E0401

dotenv_path = join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

CAMP_DB_MONGO_HOST = os.environ.get(
    "CAMP_DB_MONGO_HOST")
CAMP_DB_MONGO_PORT = os.environ.get(
    "CAMP_DB_MONGO_PORT")
CAMP_DB_MONGO_NAME = os.environ.get(
    "CAMP_DB_MONGO_NAME")
CAMP_DB_MONGO_USER = os.environ.get(
    "CAMP_DB_MONGO_USER")
CAMP_DB_MONGO_PASS = os.environ.get(
    "CAMP_DB_MONGO_PASS")


client = MongoClient("%s:%s" %
                     (CAMP_DB_MONGO_HOST, int(CAMP_DB_MONGO_PORT)))


def get_db(db=CAMP_DB_MONGO_NAME):
    db = client[db]

    db.authenticate(CAMP_DB_MONGO_USER,
                    CAMP_DB_MONGO_PASS)
    return db
