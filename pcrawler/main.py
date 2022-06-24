from asyncio import run
from pcrawler.crawler import CodeForcesCrawler, LeetCodeApiExplorer


async def fetch_codeforces():
    async with CodeForcesCrawler(1, 1, 10) as cfc:
        async for problems in cfc:
            print(problems)


async def fetch_leetcode():
    async with LeetCodeApiExplorer(1, 1, 5) as lc:
        async for problems in lc:
            print(problems)


if __name__ == '__main__':
    run(fetch_leetcode())
