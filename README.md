# async_contacts_search

Simple site parser to find contact email.

Requirements (requirements.txt):
  - pip install aiohttp
  - pip install lxml

### Crawler example:
```
cs = ContacsSearch(sites=['http://the-site.com/', ], workers=10, csv_file_name='contacts.csv')
cs.start()
```
