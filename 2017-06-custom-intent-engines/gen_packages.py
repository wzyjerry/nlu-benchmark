import os
import json

def auto_rules(query_list):
  d = {}
  for item in query_list:
    d.setdefault(item['feature'], [])
    d[item['feature']].append(item)
  count = 0
  rules = []
  for slots, result_list in d.items():
    count += 1
    rule = {
      'name': 'rule' + str(count),
      'nodes': []
    }
    nodes = rule['nodes']
    dropout = [0.0 for _ in range(len(slots) + 1)]
    content = [set() for _ in range(len(slots) + 1)]
    for result in result_list:
      for i in range(len(result['sp'])):
        sp = result['sp'][i]
        if len(result['token'][sp[0]:sp[1]]) > 0:
          content[i].add(' '.join(result['token'][sp[0]:sp[1]]))
        else:
          dropout[i] += 1
    nodes.append({
      'type': 'content',
      'value': ' | '.join(list(content[0])),
      'dropout': dropout[0] / len(result_list)
    })
    for i in range(len(slots)):
      nodes.append({
        'type': 'entity',
        'value': slots[i],
        'slot': slots[i],
        'dropout': 0.0
      })
      nodes.append({
        'type': 'content',
        'value': ' | '.join(list(content[i+1])),
        'dropout': dropout[i+1] / len(result_list)
      })
    rules.append(rule)
  return rules

def make_package(
  entitymap,
  rules,
  name='quantity',
  weight=0.01):
  package = {
    'name': name,
    'tree': {
      'intent': name,
      'type': 'intent',
      'weight': weight,
      'children': [
        {
          "type": "holder"
        }
      ]
    }
  }
  children = package['tree']['children']
  for rule in rules:
    child = {
      'type': 'order',
      'name': rule['name'],
      'dropout': 0,
      'children': []
    }
    children.append(child)
    nodes = child['children']
    for node in rule['nodes']:
      if node['dropout'] < 1.0:
        if node['type'] == 'content':
          content = node['value'].split(' | ')
          nodes.append({
            'content': content,
            'type': 'content',
            'cut': 0,
            'name': content[0],
            'dropout': node['dropout']
          })
        elif node['type'] == 'entity':
          nodes.append({
            'type': 'content',
            'cut': 0,
            'isSlot': True,
            'name': '<%s>' % node['value'],
            'entity': entitymap['%s_%s' % (name, node['value'])],
            'slot': node['slot']
          })
  return json.dumps(package)

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

def make_query_list(intent):
  queries = []
  with open(os.path.join(intent, template % intent), 'r', encoding='utf-8') as fin:
    data = json.load(fin)
    print(intent)
    for item in data[intent]:
      feature = []
      token = []
      sp = []
      st = 0
      for seg in item['data']:
        text = seg['text'].strip()
        if text == '':
          continue
        token.append(text)
        if 'entity' in seg:
          feature.append(seg['entity'])
          sp.append((st, len(token) - 1))
          st = len(token)
      sp.append((st, len(token)))
      queries.append({
        'feature': tuple(feature),
        'token': token,
        'sp': sp
      })
  return queries

OUT_DIR = 'out/packages'

def gen_packages(entity_list):
	entity_map = {x['name']: x['id'] for x in entity_list}
	for intent in intents:
		with open(os.path.join(OUT_DIR, intent), 'w', encoding='utf-8') as fout:
			fout.write(make_package(
				entity_map,
				auto_rules(make_query_list(intent)),
				name=intent,
				weight=int(100 / 7) / 100.0))
