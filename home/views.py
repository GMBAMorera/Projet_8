from urllib.parse import quote_plus
from django.shortcuts import render, redirect

from home.queries.search import Search
from home.queries.select import Select
from home.queries.pick import pick
from home.queries.find_favorites import find_favorites


# Create your views here.
def home(request, nomatch=False):
    return render(request, 'home.html', {'bad_search': bool(nomatch)})

def search(request):
    if request.method == 'POST':
        query = Search(request.POST['search'], request.user)
        if len(query.substitutes) != 0:
            # If there is acceptable result
            results = list(zip(query.substitutes, query.are_saved, query.all_url))
            return render(request, 'search.html', {
                'user': request.user,
                'results': results,
                'aliment': query.matching_query
            })
        elif query.matching_query is None:
            return redirect('nomatch', nomatch='True')
        else:
            # An aliment is found, but no aliment with better nutriscore
            url = quote_plus(query.matching_query.name)
            return redirect('nosubst', name=url, nomatch='True')

def select(request):
    if request.method == 'POST':
        selection = Select(request.POST['select'])
        print("select: ", selection.substitute.name)
        selection.select()

        url = quote_plus(selection.substitute.name)
        return redirect('aliment', name=url)

def unselect(request):
    if request.method == 'POST':
        selection = Select(request.POST['unselect'])
        print("unselect: ", selection.substitute.name)
        selection.delete()

        url = quote_plus(selection.substitute.name)
        return redirect('aliment', name=url)

def aliment(request, name, nosubst=False):
    picked_aliment = pick(name)
    print(picked_aliment.link)
    return render (request, 'aliment.html',
        {'aliment':picked_aliment, 'bad_search': bool(nosubst)})

def favorites(request):
    user = request.user
    if user.is_authenticated:
        all_fav, all_url = find_favorites(user)
        all_fav = list(zip(all_fav, all_url))
        return render(request, 'favorites.html',
            {'all_fav': all_fav, 'user': user})
    else:
        redirect('home')