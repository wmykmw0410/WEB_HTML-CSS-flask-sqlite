"""
練習問題8：config.json を作成し、json.load で読み込む — 解答

データ:
  {'app': 'MyApp', 'version': '1.0', 'debug': True}
"""
import os
import json

base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, 'config.json')

print("問題8: JSON 読み書き")

data = {'app': 'MyApp', 'version': '1.0', 'debug': True}

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(json_path, encoding='utf-8') as f:
    loaded = json.load(f)
    print(f"  app={loaded['app']}, version={loaded['version']}")

# クリーンアップ
os.remove(json_path)
