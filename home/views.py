from django.shortcuts import render

from home.search import Search

# Create your views here.
def home(request):
    return render(request, 'home.html')

def search(request):
    if request.method == 'POST':
        query = Search(request.POST['search'], request.user)
        results = list(zip(results.substitutes, results.are_saved))
        for result in results:
        return render(request, 'search.html', {
            'results': results
            'aliment': query.matching_query
        })