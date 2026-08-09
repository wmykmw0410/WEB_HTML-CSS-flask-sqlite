"""
練習問題8：config.json を作成してください

データ:
  {'app': 'MyApp', 'version': '1.0', 'debug': True}

作成後、json.load で読み込んで app と version を表示してください
"""
import os
import json

base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, 'config.json')

print("問題8: JSON 読み書き")
# TODO: json.dump で書き込み → json.load で読み込み


# クリーンアップ
if os.path.exists(json_path):
    os.remove(json_path)
