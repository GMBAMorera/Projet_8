from home.models import Aliment, Category, Substitution
from login.models import User



class Search:
    """ Results of a customer' search of substitute inside the database."""

    MAX_SUBSTITUTES = 6
    def __init__(self, form, user):
        print(form)
        self.keywords = self.extract_keywords(form)

        self.matching_query = self.get_aliment()

        self.substitutes = self.choose_substitutes()

        self.are_saved = self.check_saved(user)

    def extract_keywords(self, form):
        return form.split()

    def get_aliment(self):
        all_match = self._get_all_match()

        return self._choose_match(all_match)

    def _get_all_match(self):
        all_match = Aliment.objects.filter(name__icontains=self.keywords[0])
        for kw in self.keywords[1:]:
            all_match = all_match.filter(name__icontains=kw)
        return all_match

    def _choose_match(self, all_match):
        if all_match.exists():
            all_match = list(all_match)
            return min(all_match, key=lambda x: len(x.name))
        else:
            return None

    def choose_substitutes(self):
        if self.matching_query is not None:
            return self._choose_substitutes()
        else:
            return None

    def _choose_substitutes(self):
        all_substitute = Aliment.objects.filter(
            cat_name__exact=self.matching_query.cat_name
        ).filter(
            nutriscore__lt=self.matching_query.nutriscore
        )
        all_substitute = all_substitute.order_by('nutriscore')
        return list(all_substitute)[:self.MAX_SUBSTITUTES]

    def check_saved(self, user):
        if user.is_authenticated:
            return self._check_saved(user)
        else:
            return None

    def _check_saved(self, user):
        all_check = []
        for subst in self.substitutes:
            is_subst = Substitution.objects.filter(
                user=user, substitute=subst, original=self.matching_query
            ).exists()
            all_check.append(is_subst)
