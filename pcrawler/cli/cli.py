from asyncio import run
from enum import Enum

from typer import Typer, echo, progressbar, secho, colors

from pcrawler.cli.shell import Shell
from pcrawler.crawler import CodeForcesCrawler, LeetCodeApiExplorer
from pcrawler.data.repository import ProblemRepository

app = Typer()
repository = ProblemRepository()

crawl_sources = {
    s.__name__: s for s in (CodeForcesCrawler, LeetCodeApiExplorer)
}


class CrawlChoice(Enum):
    CodeForcesCrawler = "codeforces"
    LeetCodeApiExplorer = "leetcode"


async def crawl_source(provider_class, pages):
    with progressbar(length=pages) as bar:
        async with provider_class(1, 1, pages + 1) as provider:
            async for problems in provider:
                repository.insert(problems)
                bar.update(1)
    secho(f"Crawled {pages} pages", fg=colors.GREEN)


@app.command()
def crawl(source: CrawlChoice, pages: int = 1):
    source = crawl_sources.get(source.name)
    run(crawl_source(source, pages))


@app.command()
def shell():
    query_shell = Shell()
    query_shell.cmdloop()


if __name__ == "__main__":
    app()
