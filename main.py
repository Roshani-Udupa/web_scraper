import sys
import asyncio
from async_crawler import crawl_site_async
from json_report import write_json_report
async def main():
    if len(sys.argv) < 4:
        print("Usage: uv run main.py <url> <max_concurrency> <max_pages>")
        return

    url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])

    print(f"starting crawl of: {url}")
    print(f"Max concurrency: {max_concurrency}, Max pages: {max_pages}")

    data = await crawl_site_async(url, max_concurrency, max_pages)
    write_json_report(data)
    print("Saved the report in report.json!")

if __name__ == "__main__":
    asyncio.run(main())