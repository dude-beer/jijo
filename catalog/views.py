from django.shortcuts import render, get_object_or_404
from .models import Size, Product, Category

def home(request):
    products = (Product.objects.filter(is_active=True).select_related('category', 'color').prefetch_related('images', 'stock_items__size'))
    categories = Category.objects.all()
    return render (request, 'catalog/home.html', {'products':products, 
                                                  'categoties': categories})
    
def product_list(request):
    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category", "color")
        .prefetch_related("images", "stock_items__size")
    )

    categories = Category.objects.all()
    sizes = Size.objects.all()

    category_value = request.GET.get("category")
    size_id = request.GET.get("size")

    # Фильтр по категории
    if category_value:
        if category_value.isdigit():
            # Если передан ID, например ?category=3
            products = products.filter(
                category_id=int(category_value)
            )
        else:
            # Если передан slug, например ?category=futbolka
            products = products.filter(
                category__slug=category_value
            )

    # Фильтр по размеру
    if size_id:
        products = products.filter(
            stock_items__size_id=size_id,
            stock_items__quantity__gt=0,
        )

    return render(
        request,
        "catalog/product_list.html",
        {
            "products": products.distinct(),
            "categories": categories,
            "sizes": sizes,
            "selected_category": category_value,
            "selected_size": size_id,
        }
    )

    
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects
        .select_related("category", "color")
        .prefetch_related(
            "images",
            "stock_items__size"
        ),
        slug=slug,
        is_active=True,
    )

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
        }
    )