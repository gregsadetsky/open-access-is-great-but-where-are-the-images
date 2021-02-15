import os
import json
from tqdm import tqdm
import csv


DIR_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_DIR_PATH = os.path.join(DIR_PATH, '_data', 'all-object-json')
CSV_FILE_PATH = os.path.join(DIR_PATH, '..', '..', '1.data', 'met-images.csv')

all_object_images = []

for file_name in tqdm(os.listdir(JSON_DIR_PATH)):
  file_path = os.path.join(JSON_DIR_PATH, file_name)
  with open(file_path) as f:
    data = json.load(f)

  assert data.get('objectID')
  object_id = data['objectID']

  has_primary_image = (data['primaryImage'] != '')
  has_additional_images = (len(data['additionalImages']) != 0)

  if not has_primary_image and not has_additional_images:
    # no images for this object
    continue

  if data['primaryImage'] != '':
    all_object_images.append({
      'object_id': object_id,
      'image_url': data['primaryImage']
    })

  for image_url in data['additionalImages']:
    all_object_images.append({
      'object_id': object_id,
      'image_url': image_url
    })

with open(CSV_FILE_PATH, 'w') as f:
  writer = csv.DictWriter(f, fieldnames=('object_id', 'image_url'))
  writer.writeheader()

  for object_image in all_object_images:
    writer.writerow({
      'object_id': object_image['object_id'],
      'image_url': object_image['image_url']
    })
