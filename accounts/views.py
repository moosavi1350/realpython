from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from start_here.my_settings import MySetting


class UserRegisterView(View):
    form_class = UserRegistrationForm
    temp_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.temp_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                u = User.objects.create_user(cd['username'], cd['email'], cd['password'])
                u.first_name = cd['first_name']
                u.last_name = cd['last_name']
                u.save()
                messages.success(request, 'حساب کاربری شما ایجاد گردید. لطفا للاگین کنید', 'success')
            except Exception as ex:
                messages.error(request, 'با این نام کاربری قبلا ثبت نام شده است', 'danger')
                return redirect('accounts:user_register')
            return redirect('accounts:user_login')
        return render(request, self.temp_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    temp_name = 'accounts/login.html'
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.temp_name, {'form': form, 'bg': 'background:red'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            u = authenticate(request, username=cd['username'], password=cd['password'])
            if u is not None:
                login(request, u)
                messages.success(request, 'خوش آمدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'نام کاربری یا کلمه عبور نادرسته', 'danger')
        return render(request, self.temp_name, {'form': form, 'bg': 'background:red'})


class UserLogoutView(LoginRequiredMixin, View):
    # login_url = '/kkk/ff/'
    def get(self, request):
        logout(request)
        messages.success(request, 'به امید دیدار', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request, user_id):
        is_following = False
        tuts = request.user.tuts.all()
        m = MySetting(request)
        form = self.form_class(
            instance=request.user.profile,
            initial={'email': request.user.email, 'fn': request.user.first_name, 'ln': request.user.last_name,
                     'bg': m.setting.get('bgc'), 'fg': m.setting.get('frc')})
        # relation = Relation.objects.filter(from_user=request.user, to_user=user)
        # if relation.exists():
        #     is_following = True
        return render(request, 'accounts/profile.html',
                      {'tuts': tuts, 'is_following': is_following, 'form': form})

    def post(self, request, user_id):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.first_name = form.cleaned_data['fn']
            request.user.last_name = form.cleaned_data['ln']
            request.user.save()
            m = MySetting(request)
            m.avazkon(form.cleaned_data['bg'], form.cleaned_data['fg'])
            messages.success(request, 'پروفایل با موفقیت ذخیره شد', 'success')
        return redirect('accounts:user_profile', request.user.id)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
