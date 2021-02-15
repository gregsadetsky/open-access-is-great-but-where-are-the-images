import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os
import urllib

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# original date ranges, from the site
SEARCH_DATE_RANGES = ["8000 BCE","7000 BCE","6000 BCE","5000 BCE","4000 BCE","3000 BCE","2000 BCE","1000 BCE","1 CE","500 CE","1000 CE","1200","1400","1600","1700","1800","1900","1910","1920","1930","1940","1950","1960","1970","1980","1990","2000","2010","Present"]
# had to go 10 years at a time as the 1800-1900 range has more than 10k results
# which is the max number of results that can be returned
SEARCH_DATE_RANGES_1800 = list(map(str, range(1800, 1901, 10)))

IIIF_DOWNLOAD_URLS_OUT_PATH = os.path.join(DIR_PATH, '_data', '0.iiif-manifest-urls.txt')
IIIF_MANIFEST_URL = 'https://api.artic.edu/api/v1/artworks/{}/manifest.json'

def get_search_url(date_start, date_end, page_number):
  url_params = urllib.parse.urlencode({
    'date-start': date_start,
    'date-end': date_end,
    'page': page_number
  })
  url = 'https://www.artic.edu/collection?{}&is_public_domain=1'.format(
    url_params
  )
  return url


# return object ids, and whether there is a next page
def get_page_results_and_next_page_url(url):
  print(url)

  page_html = requests.get(url).text

  if 'Sorry, we couldn’t find any results matching your criteria' in page_html:
    return {'artwork_ids': [], 'next_page_url': None}

  page_soup = BeautifulSoup(page_html, 'html.parser')

  next_page_url = None
  # I've seen nicer code.
  res = page_soup.find_all('ul', class_='m-paginator__prev-next')
  if len(res) == 1:
    next_li = res[0].find_all('li')
    if len(next_li):
      next_li = next_li[0]
      next_span = next_li.find_all('span')[0]
      if next_span.text == 'Next':
        next_link = next_li.find_all('a')[0]
        next_page_url = next_link['href']
    else:
      print('ERR could not find ul > li')

  artwork_ids = []
  res = page_soup.find('ul', {'id': 'artworksList'})
  if res:
    listings = res.find_all('li', class_='m-listing')
    for listing in listings:
      res = re.search(r'artworks/(\d+)/', listing.find('a')['href'])
      artwork_ids.append(res.groups()[0])
  else:
    print('ERR could not find artworksList')

  return {
    'artwork_ids': artwork_ids,
    'next_page_url': next_page_url    
  }


with open(IIIF_DOWNLOAD_URLS_OUT_PATH, 'a') as f_out:
  for date_range_idx in tqdm(range(len(SEARCH_DATE_RANGES_1800) - 1)):
    date_start = SEARCH_DATE_RANGES_1800[date_range_idx]
    date_end = SEARCH_DATE_RANGES_1800[date_range_idx + 1]

    next_page_url = get_search_url(date_start, date_end, 1)
    with tqdm() as pbar:
      while next_page_url:
        results = get_page_results_and_next_page_url(next_page_url)

        for listing_id in results['artwork_ids']:
          url = IIIF_MANIFEST_URL.format(listing_id)
          f_out.write('{}\n'.format(url))

        # may be None, signalling we've iterated through all pages
        next_page_url = results['next_page_url']
        pbar.update(1)
