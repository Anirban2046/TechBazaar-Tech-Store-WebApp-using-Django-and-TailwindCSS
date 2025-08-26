from django.shortcuts import render
from store.models import Product, ReviewRating

def home(request):
    sort_option = request.GET.get('sort', 'latest')  # default: latest

    # Determine ordering based on selection
    ordering = {
        'latest': '-created_date',
        'oldest': 'created_date',
        'price_high': '-price',
        'price_low': 'price',
        'alpha_az': 'product_name',
        'alpha_za': '-product_name'
    }.get(sort_option, '-created_date')

    products = Product.objects.filter(is_available=True).order_by(ordering)[:12]

    # Compute avg_stars for each product
    for product in products:
        avg = product.averageReview()
        stars = []
        for i in range(1, 6):
            if avg >= i:
                stars.append("fa fa-star")          # full star
            elif avg >= i - 0.5:
                stars.append("fa fa-star-half-o")   # half star
            else:
                stars.append("fa fa-star-o")       # empty star
        product.avg_stars = stars
        product.review_count = product.countReview()

    context = {
        'products': products,
        'sort_option': sort_option,
    }
    return render(request, 'home.html', context)
