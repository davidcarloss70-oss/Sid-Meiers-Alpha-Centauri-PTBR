import json

cache_file = r'C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\translation_cache.json'
with open(cache_file, 'r', encoding='utf-8') as f:
    cache = json.load(f)

for k, v in cache.items():
    if k == 'COMMLINK': print(f"COMMLINK -> {v}")
    if k == 'Commlink': print(f"Commlink -> {v}")

