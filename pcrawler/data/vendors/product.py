from pcrawler.data.repository import AbstractMongoRepository


class Product:
    def __str__(self):
        return f"Product {self.__dict__}"

    def __repr__(self):
        return self.__str__()


class ProductRepository(AbstractMongoRepository):
    def insert(self, products):
        self._collection.insert_many(
            [product.__dict__ for product in products]
        )
