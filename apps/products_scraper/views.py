from django.shortcuts import render
from apps.products_scraper.models import Product
from apps.products_scraper.extract_data import main_products
from django.http import HttpResponse





# Create your views here.
def fill_database(request):
    main_products()
    context = {}
    html = "<html><body><h1>Base de datos llena</h1>.</body></html>"
    return HttpResponse(html)
    # return render(request, './filled_db.html', context)
    