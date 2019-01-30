import os
import json
import numpy as np

np.random.seed(3234764685)

intents = [
  'AddToPlaylist',
  'BookRestaurant',
  'GetWeather',
  'PlayMusic',
  'RateBook',
  'SearchCreativeWork',
  'SearchScreeningEvent'
]

template = 'train_%s.json'
template_out = 'train_70_%s.json'

data_70 = {}
for intent in intents:
  with open(os.path.join(intent, template % intent), 'r', encoding='utf-8') as fin:
    data = json.load(fin)
    print(intent)
    id_list = [i for i in range(len(data[intent]))]
    np.random.shuffle(id_list)
    data_70[intent] = [data[intent][i] for i in id_list[:70]]
    with open(os.path.join(intent, template_out % intent), 'w', encoding='utf-8') as fout:
      fout.write(json.dumps(data_70))
