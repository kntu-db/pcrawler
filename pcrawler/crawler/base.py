from abc import ABC

from aiohttp import ClientSession


class AbstractDataProvider:

    def __init__(self, current_page=1, step=1, finish_page=None):
        """
        Initialize the data provider with the current page
        """
        self.current_page = current_page
        self.step = step
        self.finish_page = finish_page
        self.__client = ClientSession()

    async def page(self, page_number):
        """
        Returns the specified page of provided data
        if no page found should raise StopAsyncIteration
        """
        raise NotImplementedError

    def get(self, url):
        """
        Get the specified url
        """
        return self.__client.get(url)

    def post(self, url, json=None):
        """
        Post the specified url
        """
        return self.__client.post(url, json=json)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        """
        Returns the next page of provided data
        if no page found should raise StopAsyncIteration
        """
        if self.finish_page and self.current_page >= self.finish_page:
            raise StopAsyncIteration
        page = await self.page(self.current_page)
        self.current_page += self.step
        return page


class AbstractWebCrawler(AbstractDataProvider, ABC):
    pass


class AbstractApiExplorer(AbstractDataProvider, ABC):
    @staticmethod
    def _json_to_entity(data):
        raise NotImplementedError
