# https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT
# https://api.binance.com/api/v3/exchangeInfo


from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
import requests as rq
from .models import Coin
from django.utils import timezone

BASE_QUERY_PRICE_URL = "https://api.binance.com/api/v3/ticker/price?symbol="
BASE_QUERY_AGAINST_SYMBOL = "USDT"


def convert(req: HttpRequest) -> HttpResponse:
    return render(req, "converter/convert.html")


def search(req: HttpRequest) -> JsonResponse:
    all_params = req.GET
    if 'coin' in all_params:
        coin_param = all_params['coin'].lower()
        coin = Coin.objects.filter(name=coin_param).first()
        if coin:
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
            coin = Coin.objects.create(
                name=coin_param,
                price=data['price'],
                updated_at=timezone.now()
            )
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
