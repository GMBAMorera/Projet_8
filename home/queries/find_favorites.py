from home.models import Substitution
from urllib.parse import quote_plus


def find_favorites(user):
    all_fav = list(Substitution.objects.filter(user=user))
    all_url = [quote_plus(fav.name) for fav in all_fav]
    return all_fav, all_url