from django.shortcuts import render
from store.models import Product, ReviewRating

def home(request):
    sort_option = request.GET.get('sort', 'latest')  # default: latest

    # Determine ordering based on selection
    if sort_option == 'latest':
        ordering = '-created_date'
    elif sort_option == 'oldest':
        ordering = 'created_date'
    elif sort_option == 'price_high':
        ordering = '-price'
    elif sort_option == 'price_low':
        ordering = 'price'
    elif sort_option == 'alpha_az':
        ordering = 'product_name'
    elif sort_option == 'alpha_za':
        ordering = '-product_name'
    else:
        ordering = '-created_date'  # fallback

    products = Product.objects.filter(is_available=True).order_by(ordering)

    # Collect reviews for all products
    reviews = ReviewRating.objects.filter(product_id__in=[p.id for p in products], status=True)

    context = {
        'products': products,
        'reviews': reviews,
        'sort_option': sort_option,
    }
    return render(request, 'home.html', context)
