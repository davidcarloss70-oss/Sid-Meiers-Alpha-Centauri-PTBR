import json

cache_file = r'C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\translation_cache.json'
with open(cache_file, 'r', encoding='utf-8') as f:
    cache = json.load(f)

def fix_string(s):
    try:
        return s.encode('latin-1').decode('utf-8')
    except:
        return s

fixed_count = 0
for k, v in cache.items():
    if 'Ã' in v:
        new_v = fix_string(v)
        if new_v != v:
            cache[k] = new_v
            fixed_count += 1
            if fixed_count <= 5:
                print(f"Fixed: {v.encode('utf-8')} -> {new_v.encode('utf-8')}")

with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print(f"Fixed {fixed_count} corrupted entries.")
