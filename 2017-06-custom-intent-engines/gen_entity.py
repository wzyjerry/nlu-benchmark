import os
import json

intents = [
  'AddToPlaylist',
  'BookRestaurant',
  'GetWeather',
  'PlayMusic',
  'RateBook',
  'SearchCreativeWork',
  'SearchScreeningEvent'
]

template = 'train_70_%s.json'

entities = {}
for intent in intents:
  with open(os.path.join(intent, template % intent), 'r', encoding='utf-8') as fin:
    data = json.load(fin)
    print(intent)
    for item in data[intent]:
      for seg in item['data']:
        if 'entity' in seg:
          entities.setdefault(seg['entity'], set())
          entities[seg['entity']].add(seg['text'].strip())

OUT_DIR = 'out/entities'
for kind in entities:
  with open(os.path.join(OUT_DIR, kind), 'w', encoding='utf-8') as fout:
    for entity in entities[kind]:
      fout.write('%s\n' % entity)
