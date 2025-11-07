import requests
import time
import json

def get_all_seller_products(token, batch_size=1000):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    headers = {"Authorization": token}
    
    all_products = []
    offset = 0
    
    while True:
        params = {
            "limit": batch_size,
            "offset": offset
        }
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if not data.get("data", {}).get("listGoods"):
            break
            
        products = data["data"]["listGoods"]
        all_products.extend(products)
        
        print(f"Получено {len(products)} товаров, всего: {len(all_products)}")
        
        if len(products) < batch_size:
            break
            
        offset += batch_size
        time.sleep(0.7)  # Соблюдение лимитов
    
    return all_products

# Использование
with open("token.txt") as f:
    token = f.read()

all_products = get_all_seller_products(token)
print(f"Всего найдено товаров: {len(all_products)}")

# Сохранение в JSON
with open("wb_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print("Товары успешно сохранены в wb_products.json")