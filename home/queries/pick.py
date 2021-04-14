from home.models import Aliment
from urllib.parse import unquote_plus


def pick(name):
    name = unquote_plus(name)
    query = Aliment.objects.filter(name__iexact=name)
    return list(query)[0]
