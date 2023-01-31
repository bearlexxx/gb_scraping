"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests
import json

url = 'https://rest.coinapi.io/v1/exchangerate/BTC?invert=false'
headers = {'X-CoinAPI-Key': '47AA7530-05A9-4D65-9124-EFBAB28CB314'}

responce = requests.get(url=url, headers=headers)

if responce.ok:
    with open(f'task_2.json', 'w', encoding='utf-8') as f:
        json.dump(responce.json(), f, indent=4, ensure_ascii=False)

    print(f'Ответ сервера  записан в файл task_2.json')
else:
    print(f'Ошибка! Код ошибки {responce.status_code}')
