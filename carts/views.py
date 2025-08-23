from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem, Wishlist, WishlistItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import _cart_id, _wishlist_id
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    product_variation = []

    if request.method == 'POST':
        # Collect variations (color, size, etc.)
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken', 'quantity']:
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    messages.error(request, "Please select Color")
                    return redirect(request.META.get('HTTP_REFERER', '/'))

        # Ensure all variation categories are selected
        required_categories = product.variation_set.values_list('variation_category', flat=True).distinct()
        selected_categories = [v.variation_category for v in product_variation]
        missing = set(required_categories) - set(selected_categories)
        if missing:
            messages.error(request, f"Please select: {', '.join(missing)}")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Handle quantity input
        quantity_input = request.POST.get('quantity')
        if quantity_input:
            try:
                quantity = int(quantity_input)
                if quantity <= 0:
                    messages.error(request, "Quantity must be greater than 0")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            except ValueError:
                messages.error(request, "Invalid quantity input.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            quantity = 1  # default increment when no input
    else:
        quantity = 1  # fallback if somehow GET request comes in


    # Authenticated user
    if current_user.is_authenticated:
        cart_item_qs = CartItem.objects.filter(product=product, user=current_user)

        if cart_item_qs.exists():
            ex_var_list = []
            id_list = []
            for item in cart_item_qs:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)

                # If user entered quantity → set, else increment
                if 'quantity' in request.POST:
                    item.quantity = quantity
                else:
                    item.quantity += quantity
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=quantity, user=current_user)
                if product_variation:
                    item.variations.set(product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=quantity, user=current_user)
            if product_variation:
                cart_item.variations.set(product_variation)
            cart_item.save()

        return redirect('cart')

    # Guest user (session cart)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        cart_item_qs = CartItem.objects.filter(product=product, cart=cart)

        if cart_item_qs.exists():
            ex_var_list = []
            id_list = []
            for item in cart_item_qs:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)

                if 'quantity' in request.POST:
                    item.quantity = quantity
                else:
                    item.quantity += quantity
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
                if product_variation:
                    item.variations.set(product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
            if product_variation:
                cart_item.variations.set(product_variation)
            cart_item.save()

        return redirect('cart')
    


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        shipping_charge = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        if total > 5000:
            shipping_charge = 0
        else:
            shipping_charge = 150
        grand_total = total + shipping_charge
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_charge'       : shipping_charge,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)



def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
    else:
        wishlist, _ = Wishlist.objects.get_or_create(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    # Collect variations
    if request.method == "POST":
        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken":
                continue
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                messages.error(request, f"Please select Color")
                return redirect(request.META.get("HTTP_REFERER", "/"))

    # Ensure all variations are selected
    all_required = product.variation_set.values_list("variation_category", flat=True).distinct()
    selected_categories = [v.variation_category for v in product_variation]
    missing = set(all_required) - set(selected_categories)
    if missing:
        messages.error(request, f"Please select: {', '.join(missing)}")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Get existing wishlist items
    if request.user.is_authenticated:
        wishlist = None
        qs = WishlistItem.objects.filter(user=request.user, product=product)
    else:
        wishlist, _ = Wishlist.objects.get_or_create(wishlist_id=_wishlist_id(request))
        qs = WishlistItem.objects.filter(wishlist=wishlist, product=product)

    # Check if same variant exists
    for item in qs:
        if list(item.variations.all()) == product_variation:
            messages.info(request, "Item already in wishlist")
            return redirect(request.META.get("HTTP_REFERER", "/"))

    # Create new wishlist item (quantity-less)
    wishlist_item = WishlistItem.objects.create(
        user=request.user if request.user.is_authenticated else None,
        wishlist=None if request.user.is_authenticated else wishlist,
        product=product
    )
    if product_variation:
        wishlist_item.variations.set(product_variation)
    wishlist_item.save()

    messages.success(request, "Item added to wishlist")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def remove_from_wishlist(request, wishlist_item_id):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id, user=request.user)
    else:
        wishlist, _ = Wishlist.objects.get_or_create(wishlist_id=_wishlist_id(request))
        wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id, wishlist=wishlist)

    wishlist_item.delete()
    messages.success(request, "Item removed from wishlist")
    return redirect("wishlist")



def move_to_cart(request, wishlist_item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id)

    product = wishlist_item.product
    product_variation = list(wishlist_item.variations.all())

    # check cart
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, product=product)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, product=product)

    # check if item already in cart with same variations
    for item in cart_items:
        existing_variations = list(item.variations.all())
        if existing_variations == product_variation:
            item.quantity += 1
            item.save()
            wishlist_item.delete()
            messages.success(request, "Item quantity updated in cart")
            return redirect("wishlist")

    # otherwise create new cart item
    if request.user.is_authenticated:
        cart_item = CartItem.objects.create(user=request.user, product=product, quantity=1)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    if product_variation:
        cart_item.variations.set(product_variation)
    cart_item.save()

    wishlist_item.delete()
    messages.success(request, "Item moved to cart")
    return redirect("wishlist")



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        shipping_charge = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        if total > 5000:
            shipping_charge = 0
        else:
            shipping_charge = 150
        grand_total = total + shipping_charge
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_charge'       : shipping_charge,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)