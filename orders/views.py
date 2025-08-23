from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import requests
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user

    # Get cart items
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    # Check stock for each cart item
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f"'{item.product.product_name}': only {item.product.stock} left in stock.")
            return redirect('cart')

    # Calculate totals
    grand_total = 0
    shipping_charge = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    shipping_charge = 0 if total > 5000 else 150
    grand_total = total + shipping_charge

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store order info
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.shipping_charge = shipping_charge
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'shipping_charge': shipping_charge,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

    return redirect('checkout')


# SSLCOMMERZ initialization remains the same
@csrf_exempt
def sslcommerz_init(request):
    if request.method == "POST":
        order_number = request.POST.get('order_id')
        try:
            order = Order.objects.get(order_number=order_number, is_ordered=False)
        except Order.DoesNotExist:
            return HttpResponse("Order not found or already processed.")

        store_id = settings.STORE_ID
        store_passwd = settings.STORE_PASSWORD
        total_amount = order.order_total

        payload = {
            'store_id': store_id,
            'store_passwd': store_passwd,
            'total_amount': total_amount,
            'currency': 'BDT',
            'tran_id': order.order_number,
            'success_url': request.build_absolute_uri(reverse('sslcommerz_success')),
            'fail_url': request.build_absolute_uri(reverse('sslcommerz_fail')),
            'cancel_url': request.build_absolute_uri(reverse('sslcommerz_cancel')),
            'cus_name': f'{order.first_name} {order.last_name}',
            'cus_email': order.email,
            'cus_add1': order.address_line_1 or 'N/A',
            'cus_add2': order.address_line_2 or '',
            'cus_city': order.city or 'Dhaka',
            'cus_state': order.state or 'Dhaka',
            'cus_postcode': '1234',
            'cus_country': order.country or 'Bangladesh',
            'cus_phone': order.phone or '01581440841',
            'shipping_method': 'NO',
            'product_name': 'Product',
            'product_category': 'Category',
            'product_profile': 'general',
        }

        try:
            response = requests.post(
                'https://sandbox.sslcommerz.com/gwprocess/v4/api.php',
                data=payload,
                timeout=10
            )
            data = response.json()
        except requests.RequestException as e:
            return HttpResponse(f"Payment gateway request failed: {e}")

        gateway_url = data.get('GatewayPageURL')
        if gateway_url:
            return redirect(gateway_url)
        else:
            return HttpResponse(f"SSLCommerz initialization failed. Response: {data}")

    return HttpResponse("Invalid request method.")


# Helper to finalize order
def finalize_order(order, payment):
    cart_items = CartItem.objects.filter(user=order.user)

    for item in cart_items:
        # Check stock again before finalizing
        if item.quantity > item.product.stock:
            messages.error(order.user, f"Cannot finalize order: '{item.product.product_name}' out of stock.")
            return

        orderproduct = OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=order.user,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
            ordered=True
        )
        orderproduct.variations.set(item.variations.all())

        # Reduce stock
        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart
    CartItem.objects.filter(user=order.user).delete()

    # Send email
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': order.user,
        'order': order,
    })
    send_email = EmailMessage(mail_subject, message, to=[order.user.email])
    send_email.send()


# Callbacks
@csrf_exempt
def sslcommerz_success(request):
    data = request.POST
    order_number = data.get('tran_id')
    val_id = data.get('val_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=False)
        payment = Payment.objects.create(
            user=order.user,
            payment_id=val_id,
            payment_method="SSLCOMMERZ",
            amount_paid=order.order_total,
            status="Completed"
        )
        order.payment = payment
        order.is_ordered = True
        order.save()

        finalize_order(order, payment)
        return redirect(f"{reverse('order_complete')}?order_number={order.order_number}&payment_id={payment.payment_id}")

    except Order.DoesNotExist:
        return redirect('home')


@csrf_exempt
def sslcommerz_fail(request):
    messages.error(request, "Payment Failed. Please try again.")
    return redirect('checkout')


@csrf_exempt
def sslcommerz_cancel(request):
    messages.warning(request, "Payment Cancelled.")
    return redirect('checkout')


@login_required
def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        payment = Payment.objects.get(payment_id=payment_id)

        ordered_products = OrderProduct.objects.filter(order=order)
        subtotal = sum([p.product_price * p.quantity for p in ordered_products])

        return render(request, 'orders/order_complete.html', {
            'order': order,
            'payment': payment,
            'ordered_products': ordered_products,
            'subtotal': subtotal,
        })

    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')
