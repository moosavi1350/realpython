from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class Tutorial(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='tuts')
    title = models.CharField(max_length=167)
    body = RichTextField()
    slug = models.SlugField(null=True, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    img = models.ImageField(upload_to='static/media/%Y/%m/', blank=True)
    imgurl = models.CharField(max_length=311, blank=True)

    class Meta:
        ordering = ('-score',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('home:details', args=(self.id, self.slug))

    def comments_count(self):
        return self.tcomments.count()


class Comment(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='ucommens')
    tut = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='tcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'
