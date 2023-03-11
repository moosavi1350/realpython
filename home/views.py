from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, Comment
from .forms import TutorialCreateForm, TutorialUpdateForm, CommentCreateForm, CommentReplyForm, TutorialSearchForm
from django.contrib import messages
from django.views import View
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests
from bs4 import BeautifulSoup


class HomeView(View):
    form_class = TutorialSearchForm

    def get(self, request):
        allT, oneT = None, None
        try:
            allT = Tutorial.objects.order_by('-created')[:9]
            # print(str(allT.query))
            oneT = allT[0]
        except Exception as ex:
            messages.error(request, ex, 'warning')
        return render(request, 'home/index.html', {'allT': allT, 'oneT': oneT, 'form': self.form_class})

class TutorialSearchView(View):
    def get(self, request):
        tuts = Tutorial.objects.filter(body__icontains=request.GET['q'])
        return render(request, 'home/search.html', {'tuts': tuts})

class DetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.tut = get_object_or_404(Tutorial, pk=kwargs['tut_id'])
        self.comments = self.tut.tcomments.filter(is_reply=False, approve=True)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'home/detail.html',
                      {'tut': self.tut, 'comments': self.comments,
                       'form': self.form_class, 'reply_form': self.form_class_reply})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.tut = self.tut
            new_comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد. بعد از تایید، نمایش داده خواهد شد', 'success')
            return redirect('home:details', self.tut.id, self.tut.slug)
        return render(request, 'home/detail.html', {'tut': self.tut, 'comments': self.comments, 'form': form})


class DeleteView(LoginRequiredMixin, View):
    def get(self, req, tut_id):
        Tutorial.objects.get(id=tut_id).delete()
        messages.warning(req, 'این مورد آموزشی با موافقیت حذف گردید', 'warning')
        return redirect('home:home')


class CreateView(LoginRequiredMixin, View):
    form_class = TutorialCreateForm
    temp_name = 'home/create.html'

    def get(self, request, page_no):
        res = {}
        # try:
        #     session = requests.Session()
        #     # r = session.get('https://realpython.com/tutorials/basics/')
        #     # r = session.get(f'https://www.mongard.ir/articles/?page={page_no}')
        #     r = session.get('https://roocket.ir/articles?category=python')
        #     content = BeautifulSoup(r.text, 'html.parser')
        #     # res = content.find( id = "the-best-way-to-get-started" )
        #     # res = content.find_all('h2', class_="card-title")
        #     # res = content('h2')
        #     res = content.find_all('h4', class_="mt-3 mb-4")
        # except Exception as N:
        #     res = N
        form = self.form_class
        return render(request, self.temp_name, {'form': form, 'res': res})

    def post(self, request, page_no):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_tut = form.save(commit=False)
            new_tut.slug = slugify(form.cleaned_data['title'][:30], allow_unicode=True)
            new_tut.save()
            messages.success(request, 'یک مورد آموزشی جدید ایجاد گردید', 'success')
            return redirect('home:home')
        return render(request, self.temp_name, {'form': form})


class UpdateView(LoginRequiredMixin, View):
    form_class = TutorialUpdateForm
    temp_name = 'home/update.html'
    
    def setup(self, request, *args, **kwargs):
        self.tut = Tutorial.objects.get(pk=kwargs['tut_id'])
        super().setup(request, *args, **kwargs)

    def get(self, request, tut_id):
        form = self.form_class(instance=self.tut)
        return render(request, self.temp_name, {'form': form})

    def post(self, request, tut_id):
        form = self.form_class(request.POST, request.FILES, instance=self.tut)
        if form.is_valid():
            new_tut = form.save(commit=False)
            new_tut.slug = slugify(form.cleaned_data['title'][:30], allow_unicode=True)
            new_tut.save()
            messages.success(request, 'اصلاحات باموافقیت ثبت گردید', 'success')
            return redirect('home:details', self.tut.id, self.tut.slug)
        return render(request, self.temp_name, {'form': form})


class TutorialAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, tut_id, comment_id):
        tut = get_object_or_404(Tutorial, pk=tut_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.tut = tut
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'پاسخ شما با موفقیت ثبت شد. بعد از تایید، نمایش داده خواهد شد', 'success')
        return redirect('home:details', tut.id, tut.slug)


def MongardArt(req, art_id, slog):
    try:
        session = requests.Session()
        r = session.get(f'https://www.mongard.ir/articles/{art_id}/{slog}/')
        content = BeautifulSoup(r.text, 'html.parser')
        res = content('main')
    except Exception as N:
        res = N
    return render(req, 'home/MongardArt.html', {'res': res})


def roocketArt(req, slog):
    try:
        session = requests.Session()
        r = session.get(f'https://roocket.ir/articles/{slog}/')
        content = BeautifulSoup(r.text, 'html.parser')
        res = content.find_all('article', class_='content-area')
    except Exception as N:
        res = N
    return render(req, 'home/roocketArt.html', {'res': res})


def not_found(request, exception):
    return render(request, '404.html')
