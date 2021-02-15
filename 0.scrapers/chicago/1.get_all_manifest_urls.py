# better way of doing this than 0.get_all_search_results........!!

import os
import json

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

JSONL_ARTWORK_DATA_PATH = os.path.join(DIR_PATH, '_data', '2.allArtworks.jsonl')
IIIF_MANIFEST_URL = 'https://api.artic.edu/api/v1/artworks/{}/manifest.json'
OUT_PATH = os.path.join(DIR_PATH, '_data', '3.all-manifest-urls.txt')

all_artwork_ids = []

with open(JSONL_ARTWORK_DATA_PATH) as f:
  for line in f:
    data = json.loads(line)
    all_artwork_ids.append(data['id'])

with open(OUT_PATH, 'w') as f:
  for artwork_id in all_artwork_ids:
    url = IIIF_MANIFEST_URL.format(artwork_id)
    f.write('{}\n'.format(url))
