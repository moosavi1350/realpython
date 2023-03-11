from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import UserRegistrationForm


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ', reverse('accounts:user_register'))
        response = self.client.get(reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.failUnless(response.context['form'], UserRegistrationForm)
        # print(response.status_code, response.context[0])

    def test_user_register_POST_valid(self):
        d = {'username': 'kk', 'email': 'k@e.com', 'password': '1', 'first_name': 'jac', 'last_name': 'j'}
        response = self.client.post(reverse('accounts:user_register'), data=d)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:user_login'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        d = {'username': 'kk', 'email': 'ppp', 'password': '1', 'first_name': 'jac', 'last_name': 'j'}
        response = self.client.post(reverse('accounts:user_register'), data=d)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='email', errors=['Enter a valid email address.'])


class TestProfileView(TestCase):
    def setUp(self):
        User.objects.create_user('root', 'root@email.com', '11')
        self.client = Client()
        self.client.login(username='root', email='root@email.com', password='11')

    def test_profile(self):
        response = self.client.get(reverse('accounts:user_profile', args='8'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
