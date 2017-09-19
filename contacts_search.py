import re
import csv
from asyncio_site_crawler import Crawler


class ContacsSearch():
    """sites - (List) List of urls
    workerts - (Int) Amount of async workers. Default is 10
    parse_pages_limit - (Int) limit of pages for parser. Default is 100
    csv_file_name - (Str) name of csv file. Default is "contacts.csv"
    """

    def __init__(self, sites, workers=10, parse_pages_limit=100, csv_file_name='contacts.csv'):
        self.sites = sites
        self.sites_contacts = {}  # {'http://site.com': {'e@mail.com', 'i@mail.com'}}
        self.workers = workers
        self.parse_pages_limit = parse_pages_limit
        self.csv_file_name = csv_file_name

    def page_handler(self, page_url, root_url, html):
        # find contacs
        p_mails = re.compile(r"""[^\s@<>"'`]+@[^\s@<>"'`]+\.[^\s@<>"'`]+""", re.MULTILINE | re.IGNORECASE)
        mails = re.findall(p_mails, html)
        if mails:
            self.sites_contacts[root_url] = set(mails)
            return True  # to close Crawler on this site

        return False  # to continue parse this site

    def save_to_csv(self):
        with open(self.csv_file_name, 'w') as csvfile:
            fieldnames = ['site', 'mails']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for site, mails in self.sites_contacts.items():
                str_mails = '|'.join(mails)
                writer.writerow({'site': site, 'mails': str_mails})

    def start(self):
        for site in self.sites:
            crawler = Crawler(
                site,
                workers=self.workers,
                parse_pages_limit=self.parse_pages_limit,
                page_handler=self.page_handler)

            crawler.crawl()

        self.save_to_csv()
