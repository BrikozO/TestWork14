import pymongo

from infrastructure.environment import env

_connector = pymongo.AsyncMongoClient(env.mongodb.uri)
quotes_db_client = _connector[env.mongodb.db]
