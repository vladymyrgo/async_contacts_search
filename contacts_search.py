import re
import csv
from asyncio_site_crawler import Crawler


class ContacsSearch():

    def __init__(self, sites, workers=10, csv_file_name='contacts.csv'):
        self.sites = sites
        self.sites_contacts = {}  # {'http://site.com': {'e@mail.com', 'i@mail.com'}}
        self.workers = workers
        self.csv_file_name

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
                page_handler=self.page_handler)

            crawler.crawl()

        self.save_to_csv()


cs = ContacsSearch(sites=['http://studioelephant.com.ua/', ], workers=10)
cs.start()
