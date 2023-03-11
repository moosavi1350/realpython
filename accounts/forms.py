from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'ltr'}), label_suffix=' *')
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={'class': 'form-control', 'dir': 'ltr'}), label_suffix=' *')
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix=' *')
    first_name = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام (اختیاری)'}))
    last_name = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'فامیلی (اختیاری)'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('ایمیل تکراری است')
        return email
    
    def clean(self):
        cd = super().clean()
        fn = cd.get('first_name')
        ln = cd.get('last_name')
        if 'hasan' in fn:
            raise ValidationError('با حسن قهرم')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری یا ایمیل', widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'ltr'}), label_suffix=' *')
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix=' *')


COLORS = (
    ("red", "قرمز"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='ایمیل')
    fn = forms.CharField(label='نام')
    ln = forms.CharField(label='فامیلی')
    # bg = forms.ChoiceField(choices=COLORS)
    bg = forms.CharField()
    fg = forms.CharField()

    class Meta:
        model = Profile
        fields = ('age', 'bio')
        labels = {'age': 'سن', 'bio': 'بیوگرافی'}
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }
