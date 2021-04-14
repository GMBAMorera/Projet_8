from home.models import Aliment, Substitution
from login.models import User


class Select:
    """
    Search for one user, one base aliment and one substitute aliment,
    then save as a new substitute or delete it.
    """

    def __init__(self, query):
        (self.user, self.substitute, self.original) = self.scrap(query)

    def scrap(self, query):
        s = self._scrap(query)
        if len(s) == 3:
            return self._find_by_components(s)
        elif len(s) == 1:
            return self._find_by_id(s[0])

    def _scrap(self, query):
        return query.split('-')

    def _find_by_id(self, substitution_id):
        substitution = self._find(substitution_id, Substitution)
        return (self._find(substitution.user.id, User),
                self._find(substitution.substitute.id, Aliment),
                self._find(substitution.original.id, Aliment))

    def _find_by_components(self, component_list):
        return (self._find(component_list[0], User),
                self._find(component_list[1], Aliment),
                self._find(component_list[2], Aliment))

    def _find(self, q, DataBase):
        try:
            return DataBase.objects.get(id=q)
        except:
            return None

    def select(self):
        Substitution.objects.get_or_create(
            user=self.user,
            substitute=self.substitute,
            original=self.original
        )

    def delete(self):
        Substitution.objects.filter(
            user=self.user,
            substitute=self.substitute,
            original=self.original
        ).delete()
