from django.test import TestCase
from accounts.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('kevin', 'kevin@email.com', '11')

    def test_ValidData(self):
        form = UserRegistrationForm(data={'username': 'jack', 'email': 'a@b.com', 'password': '1'})
        self.assertTrue(form.is_valid())

    def test_emptyData(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_existEmail(self):
        form = UserRegistrationForm(data={'username': 'jjj', 'email': 'kevin@email.com', 'password': 'xxx'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_hasan(self):
        form = UserRegistrationForm(
            data={'username': 'jack', 'email': 'a@b.com', 'password': '1', 'first_name': 'hasuuan'})
        # print('*****', form.errors, '*****')
        self.assertTrue(form.has_error)
        self.assertEqual(len(form.errors), 0)
