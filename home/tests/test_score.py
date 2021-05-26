from django.test import TestCase

from home.models import Score, Aliment, Category
from login.models import User
from home.queries import check_score
from home.constants import MEAN_VOTE, NO_VOTE


class ScoreTestCase(TestCase):
    def setUp(self):
        self.cat_test = Category.objects.create(name='cat_test')
        self.cat_test.save()

        self.aliment_test = Aliment.objects.create(name="aliment_test", nutriscore='f', ingredients='', cat_name=self.cat_test, link='link', image='image')
        self.aliment_test.save()

        self.user_test = User.objects.create(username="user_test", email="email_test", password="password_test")
        self.user_test.save()

        self.score_test = Score.objects.create(user=self.user_test, aliment=self.aliment_test, score="1")
        self.user_test.save()

    def testScore(self):
        self.assertRaises(ValueError, Score.objects.get, aliment=self.aliment_test, user=self.user_test, score="wrong_score")

    def test_check_user_score_1(self):
        assert check_score.check_user_score(self.aliment_test, self.user_test) == 1

    def test_check_user_score_2(self):
        aliment_test_2 = Aliment.objects.create(name="aliment_test_2", nutriscore='f', ingredients='', cat_name=self.cat_test, link='link', image='image')
        aliment_test_2.save()

        assert check_score.check_user_score(aliment_test_2, self.user_test) is None

    def test_check_mean_score_1(self):
        user_test_2 = User.objects.create(username="user_test_2", email="email_test", password="password_test")
        user_test_2.save()

        score_test_2 = Score.objects.create(user=user_test_2, aliment=self.aliment_test, score="2")
        score_test_2.save()

        assert check_score.check_mean_score(self.aliment_test) == MEAN_VOTE.format(1.5)

    def test_check_mean_score_2(self):
        aliment_test_2 = Aliment.objects.create(name="aliment_test_2", nutriscore='f', ingredients='', cat_name=self.cat_test, link='link', image='image')
        aliment_test_2.save()

        assert check_score.check_mean_score(aliment_test_2) == NO_VOTE

    def test_vote_for(self):
        aliment_test_2 = Aliment.objects.create(name="aliment_test_2", nutriscore='f', ingredients='', cat_name=self.cat_test, link='link', image='image')
        aliment_test_2.save()
        check_score.vote_for(self.user_test, aliment_test_2.id, "2")
        assert Score.objects.get(aliment=aliment_test_2, user=self.user_test).score == 2