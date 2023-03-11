from django import template
# import random
import datetime

register = template.Library()


@register.simple_tag
def test(x):
    w = datetime.datetime.now().weekday()
    return f'inc/navbar{w}.html'
    # return random.choice([
    #     'inc/navbar1.html',
    #     'inc/navbar2.html',
    #     'inc/navbar3.html',
    #     'inc/navbar4.html'])
