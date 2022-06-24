from .base import AbstractWebCrawler
from bs4 import BeautifulSoup
from re import search
from ..data import Problem


class CodeForcesCrawler(AbstractWebCrawler):

    @staticmethod
    def __tr_to_problem(elem):
        tds = elem.find_all('td')
        p = Problem()
        contest_code = tds[0].find('a').text.strip()
        p.contest_id = search(r'\d+', contest_code).group()
        p.code = search(r'[a-zA-Z]+', contest_code).group()
        p.title = tds[1].find_all('div')[0].find('a').text.strip()
        p.tags = [a.text.strip() for a in tds[1].find_all('div')[1].find_all('a')]
        p.difficulty = tds[3].find('span').text.strip() if tds[3].find('span') is not None else None
        p.solved = int(tds[4].find('a').text.strip().lstrip('x')) if tds[4].find('a') is not None else None
        return p

    @staticmethod
    def __get_problems(soup):
        trs = soup.find_all('tr')[1:-1]
        return [CodeForcesCrawler.__tr_to_problem(tr) for tr in trs]

    async def page(self, page_number):
        async with self.get(f"https://codeforces.com/problemset/page/{page_number}") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            return CodeForcesCrawler.__get_problems(soup)
