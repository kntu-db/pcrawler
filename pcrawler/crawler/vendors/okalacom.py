from pcrawler.crawler.base import AbstractApiExplorer
from pcrawler.data.vendors.product import Product


class OkalaApiExplorer(AbstractApiExplorer):
    API_ENDPOINT = "https://okala.com/_next/data/bKku1ZocPEiHAkR0BCfkK/search.json?page={}"
    VENDOR_ID = "OKALA"

    async def page(self, page_number):
        async with self.get(self.API_ENDPOINT.format(page_number-1)) as resp:
            response_data = await resp.json()
            return [OkalaApiExplorer._json_to_entity(data) for data in response_data['pageProps']['data']['getListOfProduct']['data']['entities']]

    @staticmethod
    def _json_to_entity(data):
        p = Product()
        p.name = data['name']
        p.caption = data['caption']
        p.barcode = data['productBarcode']
        p.vendor = OkalaApiExplorer.VENDOR_ID
        return p
