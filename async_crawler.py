import asyncio
import aiohttp
from urllib.parse import urlparse
from types import TracebackType
from crawl import PageData, extract_page_data, normalize_url, get_urls_from_html


class AsyncCrawler:
    def __init__(
        self, base_url: str, max_concurrency: int = 3, max_pages: int = 50
    ) -> None:
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks: set[asyncio.Task] = set()
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        assert self.session is not None
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if self.should_stop:
                return False

            if normalized_url in self.page_data:
                return False

            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks.copy():
                    task.cancel()
                return False

            return True

    async def get_html(self, url: str) -> str | None:
        try:
            assert self.session is not None
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status > 399:
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    return None
                return await response.text()

        except Exception:
            return None

    async def crawl_page(self, current_url: str) -> None:
        if self.should_stop:
            return

        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            return

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            if self.should_stop:
                return
            html = await self.get_html(current_url)
            if html is None:
                return
            page_info = extract_page_data(html, current_url)

            async with self.lock:
                self.page_data[normalized_url] = page_info

            next_urls = get_urls_from_html(html, self.base_url)

        tasks: list[asyncio.Task] = []

        for next_url in next_urls:
            if self.should_stop:
                break

            task = asyncio.create_task(self.crawl_page(next_url))
            self.all_tasks.add(task)

            def _cleanup(t: asyncio.Task) -> None:
                self.all_tasks.discard(t)

            task.add_done_callback(_cleanup)
            tasks.append(task)

        try:
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            for t in tasks:
                self.all_tasks.discard(t)

    async def crawl(self) -> dict[str, PageData]:
        root = asyncio.create_task(self.crawl_page(self.base_url))

        self.all_tasks.add(root)
        root.add_done_callback(lambda t: self.all_tasks.discard(t))

        try:
            await root
        except asyncio.CancelledError:
            pass

        return self.page_data


async def crawl_site_async(
    base_url: str, max_concurrency: int = 3, max_pages: int = 50
) -> dict[str, PageData]:
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
