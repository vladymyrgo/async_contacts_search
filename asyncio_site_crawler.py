#!/usr/bin/env python3
import re
import aiohttp
import asyncio
from lxml.html import fromstring
from concurrent.futures import FIRST_COMPLETED


class Crawler():
    """root_url - (Str) Site url
    workerts - (Int) Amount of async workers. Default is 10
    parse_pages_limit - (Int) limit of pages for parser. Default is 100
    page_handler - is a function to handle each page of the site.
    Must have two atrs: (url, dom)
    Example:
    ```
    def my_page_handler(url, dom):
        clean_page = dom.text_content()
        page = MyPage(url=url, body=clean_page)

    crawler = Crawler('site.com', workers=7, page_handler=my_page_handler)
    crawler.crawl()
    ```
    """

    def __init__(self, root_url, workers=10, parse_pages_limit=100, page_handler=None):
        self.workers = workers
        self.parse_pages_limit = parse_pages_limit
        self.parse_pages_counter = 0
        self.prioritized_key_words = ['contact', 'hello', 'info', 'team', 'job',
                                      'carers', 'about-us', 'aboutus']
        self.page_handler = page_handler
        self.root_url = root_url
        self.crawled_urls = set()
        self.founded_urls = set([self.root_url])
        self.url_hub = [self.root_url]
        self.allowed_regex = '\.((?!htm)(?!php)\w+)$'

        self.queue = asyncio.Queue()
        self.queue.put_nowait(self.root_url)

    @asyncio.coroutine
    def handle_task(self):
        while True:
            queue_url = yield from self.queue.get()
            self.crawled_urls.update([queue_url])
            response = yield from aiohttp.request('GET', queue_url)
            if response.status == 200:
                body = yield from response.text()
                dom = fromstring(body)

                if self.page_handler:
                    is_contacs_saved = self.page_handler(queue_url, self.root_url, body)
                    self.parse_pages_counter += 1

                    if is_contacs_saved or self.is_parse_page_limit_reached():
                        break

                self.add_new_urls_to_queue(dom=dom)

            if self.queue.empty():
                break

    def add_new_urls_to_queue(self, dom):
        new_urls_prioritized = []
        new_urls_common = []
        dom.make_links_absolute(self.root_url)
        for l in dom.iterlinks():
            newurl = l[2]
            if l[0].tag == 'a' and self.is_valid(newurl):
                if '#' in newurl:
                    newurl = newurl[:newurl.find('#')]
                self.founded_urls.update([newurl])
                for key_word in self.prioritized_key_words:
                    if key_word in newurl:
                        new_urls_prioritized.append(newurl)  # add url to prioritized list
                        break
                if newurl not in new_urls_prioritized:  # if url was not added to prioritized list
                    new_urls_common.append(newurl)  # add url to common list

        new_urls = new_urls_prioritized + new_urls_common
        for url in new_urls:
            self.queue.put_nowait(url)

    def is_valid(self, url):
            if '#' in url:
                url = url[:url.find('#')]
            if url in self.founded_urls:
                return False
            if url in self.crawled_urls:
                return False
            if self.root_url not in url:
                return False
            if re.search(self.regex, url):
                return False
            return True

    def is_parse_page_limit_reached(self):
        if self.parse_pages_counter >= self.parse_pages_limit:
            return True
        else:
            return False

    def crawl(self):
        self.regex = re.compile(self.allowed_regex)

        loop = asyncio.get_event_loop()

        tasks = [self.handle_task() for i in range(self.workers)]
        loop.run_until_complete(asyncio.wait(tasks, return_when=FIRST_COMPLETED))
