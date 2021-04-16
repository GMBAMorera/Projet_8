from django.core.management.base import BaseCommand
from requests import get
from home.models import Aliment, Category
from home.constants import (
    MAX_PRODUCTS_KEEPED, CAT_FINDING_FAIL, CAT_FINDING_SUCCESS,
    OFF_URL, PRODUCTS_FIELDS, CATEGORIES, CAT_SEARCH, PAGE_SIZE
)


class Command(BaseCommand):
    """Include at least fifty new aliments inside the Aliment table."""
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self._verify_basic_categories()

        self.add_aliments()

    def _verify_basic_categories(self):
        """ Verify if all basic categories are inside the Category table."""
        for cat in CATEGORIES:
            if not Category.objects.filter(name=cat).exists():
                self.add_category(cat)

    def add_category(self, cat):
        new_cat = Category(name=cat)
        new_cat.save()

    def add_aliments(self):
        """ Find enough data inside OpenFoodFact API
        to feed the Aliment table.
        """
        for cat in Category.objects.all():
            print(CAT_SEARCH.format(cat.name))
            n_page = 1
            counter = 0
            while counter < MAX_PRODUCTS_KEEPED:
                imported_aliments = self._scratch_category(cat.name, n_page)
                if not imported_aliments:
                    print(CAT_FINDING_FAIL.format(counter, cat.name))
                    break

                for aliment in imported_aliments:
                    if self._no_full_info(aliment):
                        continue
                    if self._redundant_info(aliment, cat):
                        continue

                    counter = self._save(aliment, cat, counter)
                n_page += 1

            print(CAT_FINDING_SUCCESS.format(cat))

    def _scratch_category(self, cat, n_page):
        """Extract one API's page of data."""
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": cat,
            "tagtype_1": "nutrition_grade",
            "tag_contains_1": "contains",
            "fields": ",".join(PRODUCTS_FIELDS),
            "page_size": PAGE_SIZE,
            "page": n_page,
            "json": "true",
        }

        al_list = get(OFF_URL, params=payload).json()
        return al_list["products"]

    def _no_full_info(self, aliment):
        for field in PRODUCTS_FIELDS:
            try:
                aliment[field]
            except KeyError:
                return True
        return False

    def _redundant_info(self, aliment, category):
        name = aliment['product_name_fr']
        ingredient = aliment['ingredients_text_fr']
        url = aliment['url']
        img = aliment['image_url']
        already_exists = Aliment.objects.filter(name__iexact=name).exists()
        if (
            name == category.name
            or already_exists
            or ingredient == ''
            or len(name) > 255
            or len(url) > 255
            or len(img) > 255
        ):
            return True
        return False

    def _save(self, aliment, category, counter):
        new_aliment = Aliment(
            name=aliment['product_name_fr'],
            nutriscore=aliment['nutrition_grade_fr'],
            ingredients = aliment['ingredients_text_fr'],
            cat_name=category,
            link= aliment['url'],
            image = aliment['image_url']
        )
        new_aliment.save()
        return counter + 1