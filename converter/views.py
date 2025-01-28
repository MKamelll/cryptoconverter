from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from . import api

# Create your views here.


def convert(req: HttpRequest) -> HttpResponse:
    return render(req, "converter/convert.html")


def search(req: HttpRequest) -> JsonResponse:
    all_params = req.GET
    if 'coin' in all_params:
        coin = all_params['coin']
        data = api.query(coin)
        return JsonResponse(data)
    return JsonResponse({'msg': "No coin was provided in query parameter", 'status': '404'})
