def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _wishlist_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
