from .models import CartItem, WishlistItem, Cart, Wishlist
from .utils import _cart_id, _wishlist_id

def counter(request):
    if 'admin' in request.path:
        return {}

    cart_count = 0
    wishlist_count = 0

    try:
        # Cart Count
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            wishlist_items = WishlistItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request)).first()

            cart_items = CartItem.objects.filter(cart=cart, is_active=True) if cart else []
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist) if wishlist else []

        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = wishlist_items.count()

    except Exception:
        cart_count = 0
        wishlist_count = 0

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }
