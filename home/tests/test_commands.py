from django.test import TestCase

from home.models import Substitution, Aliment, Category
from login.models import User

from home.management.commands import fill
from home.constatns import CATEGORIES

# Create your tests here.


class QueryTestCase(TestCase):
    def setUp(self):
        self.cat_test = Category.objects.create(name='cat_test')
        self.cat_test.save()

        self.aliment_test = Aliment.objects.create(name="aliment_test", nutriscore='f', ingredients='', cat_name=self.cat_test, link='link', image='image')
        self.aliment_test.save()

        self.substitut_test = Aliment.objects.create(name="substitut_test", nutriscore='c', ingredients='', cat_name=self.cat_test, link='link', image='image')
        self.substitut_test.save()

        self.user_test = User.objects.create(username="user_test", email="email_test", password="password_test")
        self.user_test.save()

        self.subst_test = Substitution.objects.create(user=self.user_test, substitute=self.substitut_test, original=self.aliment_test)
        self.subst_test.save()

    def test_table_list(self):
        assert self.cat_test.name in fill.Command()._table_list(Category)

    def test_add_categories(self):
        fill.Command().add_category("another_cat_test")
        test_add = Category.objects.filter(name="another_cat_test")
        assert test_add.exists()

    def test_verify_basic_categories(self):
        fill.Command()._verify_basic_categories()
        test_verify = Category.objects.filter(name="pizzas")
        assert test_verify.exists()

    def test_no_full_info_1(self):
        aliment = {
            "product_name_fr": 'test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._no_full_info(aliment) == False

    def test_no_full_info_2(self):
        aliment = {
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._no_full_info(aliment) == True

    def test_no_full_info_3(self):
        aliment = {
            "product_name_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._no_full_info(aliment) == True

    def test_no_full_info_4(self):
        aliment = {
            "product_name_fr": 'test',
            "nutrition_grade_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._no_full_info(aliment) == True

    def test_no_full_info_5(self):
        aliment = {
            "product_name_fr": 'test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._no_full_info(aliment) == True

    def test_no_full_info_6(self):
        aliment = {
        "product_name_fr": 'test',
        "nutrition_grade_fr": 'test',
        "ingredients_text_fr": 'test',
        "url": 'test',
        }
        assert fill.Command()._no_full_info(aliment) == True

    def test_redundant_info_1(self):
        category = 'test'
        aliment = {
            "product_name_fr": 'test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._redundant_info(aliment, category) == True

    def test_redundant_info_2(self):
        category = 'test'
        aliment = {
            "product_name_fr": 'another_test'*255,
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._redundant_info(aliment, category) == True

    def test_redundant_info_3(self):
        category = 'test'
        aliment = {
            "product_name_fr": 'another_test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test'*255,
            "image_url": 'test'
        }
        assert fill.Command()._redundant_info(aliment, category) == True

    def test_redundant_info_4(self):
        category = 'test'
        aliment = {
            "product_name_fr": 'another_test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'*255
        }
        assert fill.Command()._redundant_info(aliment, category) == True

    def test_redundant_info_5(self):
        al = Aliment.objects.create(name='another_test', nutriscore='f', cat_name=self.cat_test, link='', image='')
        al.save()
        category = 'test'
        aliment = {
            "product_name_fr": 'another_test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": '',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._redundant_info(aliment, category) == True

    def test_redundant_info_6(self):
        category = 'test'
        aliment = {
            "product_name_fr": 'another_test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        assert fill.Command()._redundant_info(aliment, category) == False

    def test_save_1(self):
        category = 'user_test'
        aliment = {
            "product_name_fr": 'another_test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        counter = 0
        save_counter = fill.Command()._save(aliment, category, counter)
        assert save_counter == counter + 1

    def test_save_2(self):
        category = 'user_test'
        aliment = {
            "product_name_fr": 'another_test',
            "nutrition_grade_fr": 'test',
            "ingredients_text_fr": 'test',
            "url": 'test',
            "image_url": 'test'
        }
        counter = 0
        _ = fill.Command()._save(aliment, category, counter)

        test_save = Aliment.objects.get(name='another_test')
        test_save = {
            "product_name_fr": test_save.name,
            "nutrition_grade_fr": test_save.nutriscore,
            "ingredients_text_fr": test_save.ingredients,
            "url": test_save.link,
            "image_url": test_save.image
        }
        assert aliment == test_save