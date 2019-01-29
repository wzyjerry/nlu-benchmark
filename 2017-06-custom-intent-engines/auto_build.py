import json
from urllib import request

# settings
host = '166.111.5.228'
port = 8765
agent_id = '5c4fbf68c4952f09a7d3bbd2'
api_key = 'adda9e68b1d7b08d0820c1b38405e89c81b514700f1ca9bb'

def get_entity_list():
  url = 'http://%s:%s/v1/agent/%s/entity?api_key=%s' % (host, port, agent_id, api_key)
  res = request.urlopen(url)
  return json.loads(res.read())

def create_new_intent(name, weight):
  url = 'http://%s:%s/v1/agent/%s/intent?api_key=%s' % (host, port, agent_id, api_key)
  data = {
    "weight": weight,
    "name": name,
    "tree": {
      "type": "intent",
      "weight": weight,
      "intent": name,
      "children": [{
        "type":"holder"
      }]
    }
  }
  req = request.Request(url)
  req.add_header('Content-Type', 'application/json')
  res = request.urlopen(req, json.dumps(data).encode('utf-8'))
  return json.loads(res.read())['_id']['$oid']

def create_new_entity(name, entities):
  url = 'http://%s:%s/v1/agent/%s/entity?api_key=%s' % (host, port, agent_id, api_key)
  data = {
    "entries": entities,
    "name": name
  }
  req = request.Request(url)
  req.add_header('Content-Type', 'application/json')
  request.urlopen(req, json.dumps(data).encode('utf-8'))

def put_intent(intent_id, data):
  url = 'http://%s:%s/v1/agent/%s/intent/%s?api_key=%s' % (host, port, agent_id, intent_id, api_key)
  req = request.Request(url)
  req.add_header('Content-Type', 'application/json')
  req.get_method = lambda: 'PUT'
  request.urlopen(req, data.encode('utf-8'))

import os
import gen_entity
for dirpath, dirnames, filenames in os.walk('out/entities'):
  for filename in filenames:
    with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as fin:
      entities = []
      for line in fin:
        entities.append(line)
      create_new_entity(filename, entities)
from gen_packages import gen_packages
gen_packages(get_entity_list())
for dirpath, dirnames, filenames in os.walk('out/packages'):
  for filename in filenames:
    with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as fin:
      package = fin.readline()
      data = json.loads(package)
      intent_id = create_new_intent(data['name'], data['tree']['weight'])
      put_intent(intent_id, package)
