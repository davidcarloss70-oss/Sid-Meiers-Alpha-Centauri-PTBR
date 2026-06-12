import json
import re

with open('Tools/translation_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

new_cache = {}
removed = 0

var_pattern = re.compile(r'\$[A-Z0-9_]+')

for k, v in cache.items():
    orig_vars = set(var_pattern.findall(k))
    trans_vars = set(var_pattern.findall(v))
    
    # Ignore the special gender/plural vars like $<1:has:have> for this check
    # We are just checking standard  matches
    
    if orig_vars != trans_vars:
        print(f'Removing corrupted: {k} -> {v}')
        removed += 1
    else:
        new_cache[k] = v

with open('Tools/translation_cache.json', 'w', encoding='utf-8') as f:
    json.dump(new_cache, f, indent=2, ensure_ascii=False)

print(f'Removed {removed} corrupted entries.')
