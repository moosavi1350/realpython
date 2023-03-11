from django import forms
from .models import Tutorial, Comment
from ckeditor.widgets import CKEditorWidget


class TutorialCreateForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        # fields = ['title', 'body', 'created']
        fields = '__all__'


class TutorialUpdateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Tutorial
        fields = '__all__'


class TutorialSearchForm(forms.Form):
    search = forms.CharField()


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': 'تلاش میکنم سوالات شما را در کمتر از یک روز پاسخ بدم'}
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': 'پاسخ شما به این نظر'}
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
        }
