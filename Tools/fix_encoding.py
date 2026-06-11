import json

cache_file = r'C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\translation_cache.json'
with open(cache_file, 'r', encoding='utf-8') as f:
    cache = json.load(f)

def fix_encoding(s):
    try:
        # PowerShell read UTF-8 as Windows-1252, then wrote as UTF-8.
        # So the bytes of UTF-8 were interpreted as Windows-1252 characters.
        return s.encode('cp1252').decode('utf-8')
    except:
        return s

fixed_cache = {}
fixed_count = 0
for k, v in cache.items():
    fixed_k = fix_encoding(k)
    fixed_v = fix_encoding(v)
    if fixed_k != k or fixed_v != v:
        fixed_count += 1
    fixed_cache[fixed_k] = fixed_v

with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(fixed_cache, f, ensure_ascii=False, indent=2)

print(f"Fixed {fixed_count} entries!")
