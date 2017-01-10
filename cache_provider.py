from redis import Redis


class RedisCacheProvider:
    def __init__(self, host, port, db):
        self._client = Redis(host, port, db)

    def get(self, key):
        return self._client.get(key)

    def put(self, key, value):
        # Expire time - one day
        self._client.set(name=key, value=value, ex=86400)
