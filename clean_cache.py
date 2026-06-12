import json

with open('Tools/translation_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

new_cache = {}

for k, v in cache.items():
    if '' in k or '' in k or '' in k or '' in k or '' in k or '' in k or '' in k or '' in k or '' in k:
        continue
    # also remove if it's identical but has the weird 'A A' thing
    new_cache[k] = v

with open('Tools/translation_cache.json', 'w', encoding='utf-8') as f:
    json.dump(new_cache, f, indent=2, ensure_ascii=False)

print(f'Cleaned up cache. Kept {len(new_cache)} entries out of {len(cache)}.')
