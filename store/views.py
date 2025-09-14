from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery, Variation
from category.models import Category
from carts.models import CartItem
from django.db.models import Q, Max

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from urllib.parse import urlencode

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Max
from django.db.models import Q


def store(request, category_slug=None):
    category_obj = None
    products = Product.objects.filter(is_available=True)

    # Category filter
    if category_slug:
        category_obj = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category_obj)

    # Search filter
    keyword = request.GET.get('keyword', '')
    if keyword:
        products = products.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))

    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Determine max price in current queryset
    max_product_price = products.aggregate(Max('price'))['price__max']
    if max_product_price is None:
        max_product_price = Product.objects.filter(is_available=True).aggregate(Max('price'))['price__max'] or 100000

    try:
        min_price_val = int(min_price) if min_price != '' else None
        max_price_val = int(max_price) if max_price != '' else None
        
        if max_price_val is not None and max_price_val > max_product_price:
            max_price_val = max_product_price

        if min_price_val is not None and max_price_val is not None and min_price_val > max_price_val:
            messages.error(request, "Minimum price cannot be greater!")
            base_url = request.path
            query_params = request.GET.copy()
            query_params.pop('min_price', None)
            query_params.pop('max_price', None)
            redirect_url = f"{base_url}?{query_params.urlencode()}" if query_params else base_url
            return redirect(redirect_url)

        if min_price_val is not None:
            products = products.filter(price__gte=min_price_val)
        if max_price_val is not None:
            products = products.filter(price__lte=max_price_val)

    except ValueError:
        min_price = ''
        max_price = ''
        products = products.filter(price__gte=0, price__lte=max_product_price)

    # Sorting
    sort_option = request.GET.get('sort', 'latest')
    if sort_option == 'latest':
        products = products.order_by('-id')
    elif sort_option == 'oldest':
        products = products.order_by('id')
    elif sort_option == 'price_low':
        products = products.order_by('price')
    elif sort_option == 'price_high':
        products = products.order_by('-price')
    elif sort_option == 'alpha_az':
        products = products.order_by('product_name')
    elif sort_option == 'alpha_za':
        products = products.order_by('-product_name')
    else:
        products = products.order_by('-id')  # fallback

    # Pagination: 3 per page
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # Preserve query params except page
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_params_encoded = query_params.urlencode()

    context = {
        'products': paged_products,
        'product_count': products.count(),
        'min_price': min_price,
        'max_price': max_price,
        'max_product_price': max_product_price,
        'category_obj': category_obj,
        'query_params': query_params_encoded,
        'links': Category.objects.all(),
    }
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    # Compute average rating stars
    avg = single_product.averageReview() if callable(single_product.averageReview) else single_product.averageReview
    avg_stars = []
    for i in range(1, 6):
        if avg >= i:
            avg_stars.append("fa fa-star")        # full star
        elif avg >= i - 0.5:
            avg_stars.append("fa fa-star-half-o") # half star
        else:
            avg_stars.append("fa fa-star-o")      # empty star

    # Compute stars for each review
    for review in reviews:
        rating = review.rating
        stars = []
        for i in range(1, 6):
            if rating >= i:
                stars.append("fa fa-star")
            elif rating >= i - 0.5:
                stars.append("fa fa-star-half-o")
            else:
                stars.append("fa fa-star-o")
        review.stars = stars

    # Get active variations grouped by category
    variations_by_category = {}
    for variation in single_product.variation_set.filter(is_active=True):
        cat = variation.variation_category
        variations_by_category.setdefault(cat, []).append(variation)

    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'avg_stars': avg_stars,
        'variations_by_category': variations_by_category,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    category_slug = request.GET.get('category_slug')
    return store(request, category_slug=category_slug)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        try:
            # Update existing review if exists
            review = ReviewRating.objects.get(user_id=request.user.id, product_id=product_id)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                messages.error(request, 'Please fill in all required fields.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            # Create new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
            else:
                messages.error(request, 'Please fill in all required fields.')
            return redirect(url)
    # fallback
    return redirect(url)


def search_suggestions(request):
    """AJAX view for live search suggestions"""
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if query and len(query) >= 2:  # Start suggesting after 2 characters
        products = Product.objects.filter(
            Q(product_name__icontains=query) | Q(description__icontains=query),
            is_available=True
        ).select_related('category')[:8]  # Limit to 8 suggestions
        
        for product in products:
            suggestions.append({
                'id': product.id,
                'name': product.product_name,
                'price': product.price,
                'image': product.images.url if product.images else '',
                'category': product.category.category_name,
                'url': product.get_url(),
                'stock': product.stock
            })
    
    return JsonResponse({'suggestions': suggestions})