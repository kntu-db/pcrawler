from typer import Typer, echo
from enum import Enum
from crawler import CodeForcesCrawler, LeetCodeApiExplorer


async def fetch_codeforces():
    async with CodeForcesCrawler(1, 1, 10) as cfc:
        async for problems in cfc:
            print(problems)


async def fetch_leetcode():
    async with LeetCodeApiExplorer(1, 1, 5) as lc:
        async for problems in lc:
            print(problems)


app = Typer()


class CrawlSource(Enum):
    codeforces = CodeForcesCrawler
    leetcode = LeetCodeApiExplorer


@app.command()
def crawl(source: CrawlSource):
    echo(source)


@app.command()
def shell():
    pass


if __name__ == "__main__":
    app()
