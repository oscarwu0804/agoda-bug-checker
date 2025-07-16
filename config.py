import os

# Gmail 設定
GMAIL_ACCOUNT = os.environ.get("GMAIL_ACCOUNT")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

# 城市列表（city id 可自行從 Agoda 獲取）
cities = [
    {"id": "17072", "name": "東京", "country": "日本"},
    {"id": "9395", "name": "曼谷", "country": "泰國"},
    {"id": "17062", "name": "紐約", "country": "美國"}
]
