import requests
import json
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwNTIwdjEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc3MDY4MzI4OCwiaWQiOiIwMTk4OTkxYS0zNDg0LTdiODMtOGY0YS01YWU0NmRhYzVmNzUiLCJpaWQiOjQ1NjMxNTM5LCJvaWQiOjU0MjYyOSwicyI6MTA3Mzc1Nzk1MCwic2lkIjoiMWFmM2VhOWItNzAxNC00M2ZjLThmYjEtNDc5NjExMzYyMzc3IiwidCI6ZmFsc2UsInVpZCI6NDU2MzE1Mzl9.6RDwzZtsSYBINAsNY-ZDWNQkZ7Zkzy8EdTMrX3S_LKeL06i81PzpJHsi7xgoFM0i1_4jTv-LbUR1MMbakVjzJA"

# --- Для получения данных с ценами ---
API_URL_PRODUCTS = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"

def fetch_all_products():
    offset = 0
    limit = 1000
    all_goods = []

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json"
    }

    while True:
        params = {
            "limit": limit,
            "offset": offset
        }

        response = requests.get(API_URL_PRODUCTS, headers=headers, params=params, verify=False)
        print(f"Запрос offset={offset}, статус {response.status_code}")

        if response.status_code != 200:
            print("Ошибка запроса:", response.text)
            break

        data = response.json()

        goods = data.get("data", {}).get("listGoods", [])
        if not goods:
            print("Все данные получены.")
            break

        # Фильтрация: добавляем только если цена первого размера != 0
        filtered_goods = [
            item for item in goods
            if item.get("sizes") and item["sizes"][0].get("price", 0) != 0
        ]

        all_goods.extend(filtered_goods)
        offset += limit

        if len(goods) < limit:
            print("Данные на последней странице получены.")
            break

        time.sleep(0.7)

    return all_goods

def save_products_to_file(data, filename="wildberries_all_products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено {len(data)} товаров с ценами в файл {filename}")

# --- Для получения карточек с фото и прочим ---
API_URL_CARDS = "https://content-api.wildberries.ru/content/v2/get/cards/list"

HEADERS_CARDS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def fetch_all_cards():
    all_cards = []
    limit = 100
    cursor = {
        "limit": limit
        # "updatedAt" и "nmID" добавим после первого запроса для пагинации
    }

    while True:
        payload = {
            "settings": {
                "filter": {
                    "withPhoto": -1  # получить все карточки
                },
                "cursor": cursor
            }
        }

        response = requests.post(API_URL_CARDS, headers=HEADERS_CARDS, json=payload, verify=False)
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code} - {response.text}")
            break

        data = response.json()

        cards = data.get("cards", [])
        if not cards:
            print("Карточек больше нет.")
            break

        all_cards.extend(cards)

        cursor_info = data.get("cursor", {})
        updatedAt = cursor_info.get("updatedAt")
        nmID = cursor_info.get("nmID")
        total = cursor_info.get("total", 0)

        # Обновляем курсор для следующего запроса
        cursor["updatedAt"] = updatedAt
        cursor["nmID"] = nmID

        print(f"Получено карточек: {len(all_cards)}, следующий курсор: updatedAt={updatedAt}, nmID={nmID}")

        # Если количество полученных карточек на последней странице меньше лимита — закончить
        if total < limit:
            print("Все карточки получены.")
            break

        time.sleep(0.6)  # чтобы не превышать лимит 100 запросов в минуту

    return all_cards

def save_cards_to_file(data, filename="wb_cards_all.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено {len(data)} карточек в файл {filename}")

# --- Основной запуск ---
if __name__ == "__main__":
    print("=== Получение данных с ценами ===")
    products = fetch_all_products()
    if products:
        save_products_to_file(products)
    else:
        print("Данные с ценами не получены.")

    print("\n=== Получение карточек с фото ===")
    cards = fetch_all_cards()
    if cards:
        save_cards_to_file(cards)
    else:
        print("Карточки не получены.")
