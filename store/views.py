from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator
# Create your views here.

def store(request, category_slug=None):
    
    products = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available = True, category=category)
        page = request.GET.get('page')
        print(page)
        paginator = Paginator(products, 1)
        page_product = paginator.get_page(page)
    else:
        products = Product.objects.filter(is_available = True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)
        for i in page_product:
            print(i)
            print(page_product.has_next(), page_product.has_previous(), page_product.previous_page_number, page_product.next_page_number)
        
    categories = Category.objects.all()
    context = {'products' : page_product, 'categories' : categories,}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = Product.objects.get(slug=product_slug, category__slug=category_slug)
    return render(request,'store/product-detail.html', {'product' : single_product})