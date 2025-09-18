import pymongo

from infrastructure.environment import env

_connector_async = pymongo.AsyncMongoClient(env.mongodb.uri)
quotes_db_client_async = _connector_async[env.mongodb.db]

_connector = pymongo.MongoClient(env.mongodb.uri)
quotes_db_client = _connector[env.mongodb.db]
