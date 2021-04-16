from django.test import TestCase
from django.test import Client

from home.models import Substitution, Aliment, Category
from login.models import User

from home.queries.find_favorites import find_favorites
from home.queries.pick import pick
from home.queries.search import Search
from home.queries.select import Select
from urllib.parse import quote_plus

# Create your tests here.


class QueryTestCase(TestCase):
    def setUp(self):
        self.user_test = User.objects.create_user(username="user_test", email="email_test", password="pasword_test")
        self.user_test.save()
        self.client = Client()

        self.cat_test = Category.objects.create(name='cat_test')
        self.cat_test.save()
        self.aliment_test = Aliment.objects.create(name="aliment_test", nutriscore='f', ingredients='', cat_name=self.cat_test, link='link', image='image')
        self.aliment_test.save()
        self.substitut_test = Aliment.objects.create(name="substitut_test", nutriscore='c', ingredients='', cat_name=self.cat_test, link='link', image='image')
        self.substitut_test.save()

        self.match = Search("aliment_test", self.user_test)

    def test_find_favorites(self):
        self.subst_test = Substitution.objects.create(user=self.user_test, substitute=self.substitut_test, original=self.aliment_test)
        self.subst_test.save()
        all_fav, _ = find_favorites(self.user_test)
        assert self.subst_test in all_fav

    def test_pick(self):
        name = quote_plus(self.aliment_test.name)
        al = pick(name)
        assert self.aliment_test == al

    def test_extract_keywords(self):
        kw = Search("tarte tatin", self.user_test).extract_keywords("tarte tatin")
        assert kw == "tarte tatin".split()

    def test_match_1(self):
        assert self.match.matching_query == self.aliment_test

    def test_match_2(self):
        match = Search("substitut_test pas cette fois", self.user_test)
        assert match.matching_query == None

    def test_match_3(self):
        match = Search("rien", self.user_test)
        assert match.matching_query == None

    def test_substitutes_1(self):
        self.match.matching_query = None
        substitutes = self.match.choose_substitutes()
        assert substitutes == []

    def test_substitutes_2(self):
        assert self.substitut_test in self.match.substitutes

    def test_check_saved_1(self):
        assert self.match.are_saved == [False]

    def test_check_saved_2(self):
        self.client.login(username=self.user_test.username, password=self.user_test.password)
        assert self.match.check_saved(self.user_test) == [False]

    def test_check_saved_3(self):
        self.subst_test = Substitution.objects.create(user=self.user_test, substitute=self.substitut_test, original=self.aliment_test)
        self.subst_test.save()
        self.client.login(username=self.user_test.username, password=self.user_test.password)
        all_check = self.match.check_saved(self.user_test)
        assert all_check == [True]

    def test_build_all_url(self):
        assert quote_plus(self.match.substitutes[0].name) in self.match.all_url 

    def test_scrap(self):
        test = "test1-test2-test3"
        assert test.split('-') == Select(test)._scrap(test)

    def test_find(self):
        test = "test1-test2-test3"
        assert self.aliment_test == Select(test)._find(self.aliment_test.id, Aliment)

    def test_select(self):
        test = Select(f'{self.user_test.id}-{self.substitut_test.id}-{self.aliment_test.id}')
        test.select()
        assert Substitution.objects.filter(user=self.user_test, substitute=self.substitut_test, original=self.aliment_test).exists()

    def test_delete(self):
        self.subst_test = Substitution.objects.create(user=self.user_test, substitute=self.substitut_test, original=self.aliment_test)
        self.subst_test.save()
        test = Select(f'{self.subst_test.id}')
        test.delete()
        assert not Substitution.objects.filter(user=self.user_test, substitute=self.substitut_test, original=self.aliment_test).exists()
