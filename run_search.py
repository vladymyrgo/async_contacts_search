from contacts_search import ContacsSearch
from search_list import SITES_LIST


CHUNK_SIZE = 200
WORKERS = 10
PARSE_PAGES_LIMIT = 200


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


for idx, search_list in enumerate(chunks(SITES_LIST, CHUNK_SIZE)):
    start = (CHUNK_SIZE * (idx + 1)) - CHUNK_SIZE
    end = CHUNK_SIZE * (idx + 1)
    filename = 'contacts_{}_{}.csv'.format(start, end)
    cs = ContacsSearch(sites=search_list, workers=WORKERS, parse_pages_limit=PARSE_PAGES_LIMIT, csv_file_name=filename)
    cs.start()
