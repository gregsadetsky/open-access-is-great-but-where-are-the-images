import os
import json
from tqdm import tqdm
import csv

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FILES_PATH = os.path.join(DIR_PATH, '_data', 'all-iiif-manifest')

CSV_FILE_OUT = os.path.join(DIR_PATH, '..', '..', '1.data', 'chicago-images.csv')

object_images = []

for file_name in tqdm(os.listdir(DATA_FILES_PATH)):
  file_path = os.path.join(DATA_FILES_PATH, file_name)
  with open(file_path) as f:
    data = json.load(f)

  assert data.get('metadata')
  object_number = list(filter(lambda _: _['label'] == 'Object Number', data['metadata']))
  assert len(object_number) == 1
  object_number = object_number[0]['value']

  assert data.get('sequences'), file_name
  assert len(data['sequences']) == 1, file_name
  if not data['sequences'][0].get('canvases'):
    # no images at all
    continue

  all_image_urls = []

  for canvas in data['sequences'][0]['canvases']:
    assert canvas.get('images'), file_name
    assert len(canvas['images']) == 1, file_name
    assert canvas['images'][0].get('resource'), file_name
    assert canvas['images'][0]['resource'].get('@id'), file_name
    image_url = canvas['images'][0]['resource']['@id']
    assert image_url.endswith('default.jpg'), file_name
    all_image_urls.append(image_url)

  object_images.append({
    'object_number': object_number,
    'all_image_urls': all_image_urls
  })

with open(CSV_FILE_OUT, 'w') as f:
  writer = csv.DictWriter(f, fieldnames=('object_number', 'image_url'))
  writer.writeheader()

  for object_image in tqdm(object_images):
    for image_url in object_image['all_image_urls']:
      writer.writerow({
        'object_number': object_image['object_number'],
        'image_url': image_url
      })
