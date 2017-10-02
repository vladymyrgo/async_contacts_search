# async_contacts_search

Simple site parser to find contact email.

Requirements (requirements.txt):
  - pip install aiohttp
  - pip install lxml

### Crawler example:
```
from contacts_search import ContacsSearch
cs = ContacsSearch(sites=['http://the-site.com/', ], workers=10, csv_file_name='contacts.csv')
cs.start()  # create csv file
```

### CSV file reader example:
```
from csv_contacts_reader import CSVContactsReader
reader = CSVContactsReader('contacts_csv/02_10_17/contacts_total.csv')
contacts = reader.get_clean_contacts()  # return dict like: {site_url: set(mail1, mail2)}
```

### run_search.py
Run the file to make a search (first: add list of sites to search_list.py)
