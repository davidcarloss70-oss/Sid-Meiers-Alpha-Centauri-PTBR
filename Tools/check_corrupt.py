import json
import re

cache_file = r'C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\translation_cache.json'
with open(cache_file, 'r', encoding='utf-8') as f:
    cache = json.load(f)

corrupted = []
for k, v in cache.items():
    if 'Ã' in v:
        corrupted.append((k, v))

print(f"Found {len(corrupted)} corrupted entries.")
for k, v in corrupted[:10]:
    print(f"{k} -> {v}")
