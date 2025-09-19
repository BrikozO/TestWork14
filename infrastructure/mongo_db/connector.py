import threading

import pymongo

from infrastructure.environment import env


class MongoDBConnector:
    def __init__(self, conn_uri: str, db_name: str):
        self._conn_uri = conn_uri
        self._db_name = db_name
        self._sync_db_client = None
        self._async_db_client = None
        self._lock = threading.Lock()

    def get_sync_connection(self):
        if not self._sync_db_client:
            with self._lock:
                if not self._sync_db_client:
                    _connector = pymongo.MongoClient(env.mongodb.uri)
                    self._sync_db_client = _connector[self._db_name]
        return self._sync_db_client

    async def get_async_connection(self):
        if not self._async_db_client:
            _connector_async = pymongo.AsyncMongoClient(env.mongodb.uri)
            self._async_db_client = _connector_async[self._db_name]
        return self._async_db_client


conn = MongoDBConnector(env.mongodb.uri, env.mongodb.db)
