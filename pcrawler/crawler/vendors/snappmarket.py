from pcrawler.crawler.base import AbstractApiExplorer
from pcrawler.data.vendors.product import Product


class SnappMarketApiExplorer(AbstractApiExplorer):
    API_ENDPOINT = "https://core.snapp.market/api/v2/vendors/pznjk2/products?limit={}&offset={}&categories[]=278353"
    VENDOR_ID = "SNPMRKT"
    PAGE_SIZE = 50

    async def page(self, page_number):
        async with self.get(self.API_ENDPOINT.format(self.PAGE_SIZE, (page_number - 1) * self.PAGE_SIZE)) as resp:
            response_data = await resp.json()
            return [SnappMarketApiExplorer._json_to_entity(data) for data in response_data['results']]

    @staticmethod
    def _json_to_entity(data):
        p = Product()
        p.name = data['title']
        p.vendor = SnappMarketApiExplorer.VENDOR_ID
        return p
