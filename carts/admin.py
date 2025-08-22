from django.contrib import admin
from .models import Cart, CartItem, Wishlist, WishlistItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id', 'date_added')
    
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'wishlist', 'added_on')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)