from asyncio import run
from enum import Enum

from typer import Typer, progressbar, secho, colors

# from pcrawler.cli.shell import Shell
from pcrawler.crawler import OkalaApiExplorer, SnappMarketApiExplorer
from pcrawler.data.vendors.product import ProductRepository as Repository

app = Typer()
repository = Repository()

crawl_sources = {
    s.__name__: s for s in (OkalaApiExplorer, SnappMarketApiExplorer, )
}


class CrawlChoice(Enum):
    OkalaApiExplorer = "okala"
    SnappMarketApiExplorer = "snappmarket"


async def crawl_source(provider_class, pages, start_page=1):
    with progressbar(length=pages) as bar:
        async with provider_class(start_page, 1, pages + 1) as provider:
            async for entities in provider:
                repository.insert(entities)
                bar.update(1)
    secho(f"Crawled {pages} pages", fg=colors.GREEN)


@app.command()
def crawl(source: CrawlChoice, pages: int = 1):
    source = crawl_sources.get(source.name)
    run(crawl_source(source, pages))


# @app.command()
# def shell():
#     query_shell = Shell()
#     query_shell.cmdloop()


if __name__ == "__main__":
    app()
