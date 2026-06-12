import json
with open('Tools/translation_cache.json', encoding='utf-8') as f:
    data = json.load(f)
print(data['As to myself, I remain $TITLE2 $NAME3 of the $FACTION4. My intention'])
