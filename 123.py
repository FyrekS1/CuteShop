import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import time

# 🔑 ВСТАВЬ СЮДА токен AuthorizeV3
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTAyMjQ1OTAsInVzZXIiOiI0NTYzMTUzOSIsInNoYXJkX2tleSI6IjI3IiwiY2xpZW50X2lkIjoic2VsbGVyLXBvcnRhbCIsInNlc3Npb25faWQiOiI4M2Y1MzY4NzM5ZTI0ZWE1YmRmYmM2YjkxN2Y3YTJjYyIsInZhbGlkYXRpb25fa2V5IjoiMTcyMTY0YTlhMzM0ZjkzZjg0OWMxYmU5Y2RiM2NiMDNiNTkwNjkxMzUzNjE0MDM1ZjRkNzg5ZTJlZmJlNWJhNSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjcxOTg0NjE3LCJ2ZXJzaW9uIjoyfQ.HWJGe7zs2CQahwFT6OCsJSeJd8bDaopDHwbZMgspZFXeFdn85eM5a1z1D83j391jhMXE9zgPFQ9whGlDRQDDa40ZnkJaNqOGy_QE9-IuoPUIlHNQJ3JWTebuENM4C1kqyCbAFREB8Nc3jMmWxYwdcWvDFu6JMhq56iG3lAB1IGUj_xe_5HVdHK162hxcS-fGuFZBTg90_2vGr4hVPdXuoLopOl0JUaEwxfdcRuoqiIEtQ2Rt_YIPZYWNvR67wy66-pB25iR1G7bwMzc2Noyh8kUFera2XJud8D-GNWH3dvzlUtIJPNmxcbTRBq7vhVJaqhdeVqb99YURj1ADeUQt8Q"

# 🍪 ВСТАВЬ СЮДА куки в формате словаря
COOKIES = {
    "current_feature_version": "103745CF-21F2-4BE7-8581-DE18BA8DDBBC",
    "external-locale": "ru",
    "_wbauid": "62254361750150917",
    "landing_version_ru": "EFD8FA05-7358-4E4C-9DE8-5608214FE1E4",
    "wbx-validation-key": "a79eb215-329e-47b8-89c3-1329d7b9c412",
    "locale": "ru",
    "x-supplier-id": "1af3ea9b-7014-43fc-8fb1-479611362377",
    "x-supplier-id-external": "1af3ea9b-7014-43fc-8fb1-479611362377",
    "device_id_guru": "1977d215e9f-376283190137a042",
    "client_ip_guru": "79.133.156.200"
}

HEADERS = {
    "AuthorizeV3": TOKEN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Origin": "https://seller.wildberries.ru",
    "Referer": "https://seller.wildberries.ru/",
    "Content-Type": "application/json"
}

print("[1/2] Генерация шаблона...")
init_url = "https://discounts-prices.wildberries.ru/ns/dp-api/discounts-prices/suppliers/api/v1/list/goods/excel?bySize=false"
resp = requests.get(init_url, headers=HEADERS, cookies=COOKIES, verify=False)
print("Ответ:", resp.status_code)

print("[Ждём 3 секунды пока Wildberries сформирует файл...]")
time.sleep(3)

print("[2/2] Скачивание готового файла...")
result_url = "https://discounts-prices.wildberries.ru/ns/dp-api/discounts-prices/suppliers/api/v1/list/goods/excel/result?bySize=false"
resp = requests.get(result_url, headers=HEADERS, cookies=COOKIES, verify=False)

if resp.status_code == 200:
    with open("wb_template.txt", "wb") as f:
        f.write(resp.content)
    print("✅ Готово! Файл сохранён как wb_template.txt")
else:
    print(f"❌ Ошибка при скачивании файла: {resp.status_code}")




import json
import base64

# Открываем файл с JSON (который ты переименовал в .txt)
with open("wb_template.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

# Достаём base64 строку
base64_excel = data["data"]["listGoodsExcel"]

# Декодируем и сохраняем
with open("wb_template.xlsx", "wb") as f_out:
    f_out.write(base64.b64decode(base64_excel))

print("✅ Готово: wb_template.xlsx сохранён.")


import pandas as pd

# Читаем файл Excel
df = pd.read_excel("wb_template.xlsx")

# Сохраняем в JSON (один из вариантов)
df.to_json("wb_template.json", orient="records", force_ascii=False, indent=2)

print("✅ wb_template.json сохранён.")
