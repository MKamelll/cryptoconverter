from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
import requests as rq
from .models import Coin
from django.utils import timezone

BASE_QUERY_PRICE_URL = "https://api.binance.com/api/v3/ticker/price?symbol="
BASE_QUERY_AGAINST_SYMBOL = "USDT"
BASE_URL_ALL_COINS_INFO = "https://api.binance.com/api/v3/exchangeInfo"


def convert(req: HttpRequest) -> HttpResponse:
    return render(req, "converter/convert.html")


def update_db_with_new_coins(req: HttpRequest) -> JsonResponse:
    res = rq.get(BASE_URL_ALL_COINS_INFO)
    if res.status_code == 200:
        data = res.json()
        new_coins: list[Coin] = []
        if 'symbols' in data:
            pairs_info = data['symbols']
            for i, _ in enumerate(pairs_info):
                sym = pairs_info[i]['symbol']
                if sym.endswith(BASE_QUERY_AGAINST_SYMBOL):
                    coin = sym[:-4].lower()
                    coin_created = Coin.objects.filter(name=coin).first()
                    if not coin_created:
                        new_coin_created = Coin(
                            name=coin,
                            price="",
                            updated_at=timezone.now()
                        )
                        new_coins.append(new_coin_created)
            Coin.objects.bulk_create(new_coins)
        return JsonResponse({
            'status': 200
        })
    return JsonResponse({
        'msg': res.json()['msg'],
        'status': 404

    })


def search(req: HttpRequest) -> JsonResponse:
    all_params = req.GET
    if 'coin' in all_params:
        coin_param = all_params['coin'].lower()
        coin = Coin.objects.filter(name=coin_param).first()
        print(coin)
        if coin and len(coin.price) > 0:
            duration = timezone.now() - coin.updated_at
            if duration.seconds < 5 * 60:
                return JsonResponse({
                    'price': coin.price,
                    'status': 200
                })

        res = rq.get(BASE_QUERY_PRICE_URL + coin_param.upper() +
                     BASE_QUERY_AGAINST_SYMBOL)
        if res.status_code == 200:
            data = res.json()
            coin = Coin.objects.filter(name=coin_param).first()
            if not coin:
                new_coin = Coin.objects.create(
                    name=coin_param,
                    price=data['price'],
                    updated_at=timezone.now()
                )
                new_coin.save()
            elif len(coin.price) <= 0:
                coin.price = data['price']
                coin.save()

            return JsonResponse({
                'price': data['price'],
                'status': 200
            })
        else:
            return JsonResponse({
                'msg': res.json()['msg'],
                'status': 404
            })
    return JsonResponse({'msg': "No coin was provided in query parameter", 'status': '404'})
