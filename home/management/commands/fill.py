from django.core.management.base import BaseCommand, CommandError
from requests import get
from home.models import Aliment, Category
from home.management.commands.constants import (
    MAX_PRODUCTS_KEEPED, CAT_FINDING_FAIL, CAT_FINDING_SUCCESS,
    OFF_URL, PRODUCTS_FIELDS, CATEGORIES, CAT_SEARCH, PAGE_SIZE
)


class Command(BaseCommand):
    """Include at least fifty new aliments inside the Aliment table."""
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.all_aliments = self._table_list(Aliment)

        self.all_categories = self._table_list(Category)
        self._verify_basic_categories()

        self.add_aliments()

    def _table_list(self, Table):
        """ return a list of row names inside a table.
        Should only be used with Aliment of Category table.
        """
        return [a.name for a in Table.objects.all()]

    def _verify_basic_categories(self):
        """ Verify if all basic categories are inside the Category table."""
        for cat in CATEGORIES:
            if cat not in self.all_categories:
                new_cat = Category(name=cat)
                new_cat.save()
        self.all_categories = self._table_list(Category)

    def add_aliments(self):
        """ Find enough data inside OpenFoodFact API
        to feed the Aliment table.
        """
        for cat in self.all_categories:
            print(CAT_SEARCH.format(cat))
            n_page = 1
            counter = 0
            while counter < MAX_PRODUCTS_KEEPED:
                imported_aliments = self._scratch_category(cat, n_page)
                if not imported_aliments:
                    print(CAT_FINDING_FAIL.format(counter, cat))
                    break

                counter = self._try_aliment_list(imported_aliments, cat, counter)
                n_page += 1

            print(CAT_FINDING_SUCCESS.format(cat))

    def _scratch_category(self, cat, n_page):
        """Extract one page of data of the API."""
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

    def _try_aliment_list(self, al_list, cat, counter):
        """Check and save all data complete enough to be used
        on Pur Beurre, discarding them otherwise.
        """
        for al in al_list:
            try:
                name, nut, ing, url = self._create_row(al)
            except KeyError:
                continue

            if self._incorrect_product(name, cat, ing, url):
                continue

            counter += 1

            new_aliment = Aliment(
                name=name,
                nutriscore=nut,
                ingredients = ing,
                cat_name=Category.objects.get(name=cat),
                link=url
            )
            new_aliment.save()
            self.all_aliments = self._table_list(Aliment)
        return counter

    def _incorrect_product(self, name, cat, ing, url):
        if (
            name == cat 
            or name in self.all_aliments
            or ing == ''
            or len(name) > 255
            or len(url) > 255
        ):
            return True
        return False

    def _create_row(self, al):
        """ Format data along a VALUE mysql instruction."""
        return (
            al['product_name_fr'],
            al['nutrition_grade_fr'],
            al['ingredients_text_fr'],
            al['url']
        )