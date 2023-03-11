from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.db import connection


class StartHereView(View):
    def get(self, request):
        users = User.objects.all().count()
        return render(request, 'start_here/start_here.html', {'users': users})

# def start_here(request):
#     cursor = connection.cursor()
#     # cursor.execute(''' ''')
#     # cursor.execute(''' ''')
#     # row = cursor.fetchone()
#     # print(row)
#     return render(request, 'start_here/start_here.html')


def community(request):
    return render(request, 'start_here/community.html')
