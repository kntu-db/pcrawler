import abc

from .client import get_client


class AbstractMongoRepository(abc.ABC):
    @property
    def _client(self):
        if not hasattr(self, "__client"):
            self.__client = get_client()
        return self.__client

    @property
    def _db(self):
        return self._client["pcrawler"]

    @property
    def _collection_name(self):
        return self.__class__.__name__.replace("Repository", "").lower()

    @property
    def _collection(self):
        return self._db[self._collection_name]
