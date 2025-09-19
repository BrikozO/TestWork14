from pymongo.asynchronous.database import AsyncDatabase


async def create_unique_index(client: AsyncDatabase, collection: str, keys: list[str]):
    coll = client[collection]
    await coll.create_index(keys=keys, unique=True)
