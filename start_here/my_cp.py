# My context_processors
from .my_settings import MySetting


def myFunc(request):
    return {'mykey': 76}


def mySett(request):
    m = MySetting(request)
    return {'mys': m.setting}
