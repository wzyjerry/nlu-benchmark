import json
with open('AddToPlaylist/train_70_AddToPlaylist.json', 'r', encoding='utf-8') as fin:
  data = json.loads(fin.readline())
  print(len(data['AddToPlaylist']))
