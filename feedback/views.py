from django.shortcuts import render
from django.views import View
from .models import Feedback
from django.contrib import messages


class FeedbackView(View):
    def get(self, req):
        return render(req, 'feedback/feedback.html')

    def post(self, req):
        Feedback.objects.create(body=req.POST['feedback'], name=req.POST['name'], email=req.POST['contact_info'],)
        messages.success(req, 'نظر شما ثبت گردید', 'success')
        return render(req, 'feedback/feedback.html')
