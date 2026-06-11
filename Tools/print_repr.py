import json

cache_file = r'C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\translation_cache.json'
with open(cache_file, 'r', encoding='utf-8') as f:
    cache = json.load(f)

for k, v in cache.items():
    if 'Ã' in v:
        print(repr(v.encode('utf-8')))
        break
