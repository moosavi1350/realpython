from django.test import TestCase
from home.models import Comment, Tutorial
from django.contrib.auth.models import User
from model_bakery import baker


class TestCommentModel(TestCase):

    def setUp(self):
        user = baker.make(User, username='zz')
        # print('*****', user.password, '*****')
        tut = baker.make(Tutorial, user=user, body='bbb')
        # print('*****', tut, '*****')
        self.comment = baker.make(Comment, user=user, tut=tut)
        # print('*****', comment.body, '*****')

    def test_model_str(self):
        self.assertEqual(str(self.comment), f'zz - {self.comment.body[:30]}')
