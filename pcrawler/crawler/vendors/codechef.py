from hashlib import sha1
from pcrawler.crawler.base import AbstractApiExplorer
from pcrawler.data import Problem
from datetime import datetime
from requests import get


class CodeChefApiExplorer(AbstractApiExplorer):

    ENDPOINT = "https://www.codechef.com/api/list/problems?page={}&limit={}&sort_by=difficulty_rating&sort_order=asc&search=&category=rated&start_rating=0&end_rating=999&topic=&tags=&group=all&"

    @staticmethod
    def _json_to_entity(data):
        p = Problem()
        p.id = int(data['id'])
        p.title = data['name']
        p.difficulty = int(data['difficulty_rating'])
        p.solved = int(data['successful_submissions']) if data['successful_submissions'] else None
        p.total = int(data['total_submissions']) if data['total_submissions'] else None
        p.tags = []
        p.time_step = datetime.now()
        p.site = 'codechef'
        p.uid = sha1((p.site + p.title).encode('UTF-8')).hexdigest()
        return p

    PAGE_SIZE = 50

    async def page(self, page_number):
        resp = get(self.ENDPOINT.format(page_number-1, self.PAGE_SIZE))
        response_data = resp.json()
        return [CodeChefApiExplorer._json_to_entity(data) for data in response_data['data']]
