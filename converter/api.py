"""https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"""
import requests as rq


def generate_url(coin: str) -> str:
    return f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}USDT"


def query(coin: str) -> dict[str, str]:
    url = generate_url(coin)
    res = rq.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            'price': data['price'],
            'status': '200'
        }
    return {
        'msg': res.json()['msg'],
        'status': '404'
    }
