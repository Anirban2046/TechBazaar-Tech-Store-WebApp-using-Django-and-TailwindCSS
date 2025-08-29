from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from orders.models import Order, OrderProduct
from django.contrib import messages, auth
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Email & verification utils
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.cache import cache
import random
import time
import requests

from carts.views import _cart_id
from carts.models import Cart, CartItem


# Registration with OTP
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.is_active = False
            user.save()

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            cache.set(f"email_otp_{user.id}", otp, timeout=180)  # store OTP
            request.session['temp_user_id'] = user.id
            request.session['otp_expiry'] = int(time.time()) + 180  # store expiry for timer

            # Send Email
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
            )

            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'activation_link': activation_link,
                'otp': otp,
            })
            EmailMessage(mail_subject, message, to=[email]).send()

            messages.success(request, 'We sent you a verification email with a link and an OTP.')
            return redirect('verify_otp')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('temp_user_id')

        if not user_id:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        cached_otp = cache.get(f"email_otp_{user_id}")
        if cached_otp and entered_otp == cached_otp:
            try:
                user = Account.objects.get(id=user_id)
                user.is_active = True
                user.save()

                auth_login(request, user)
                cache.delete(f"email_otp_{user_id}")  # cleanup
                request.session.pop('temp_user_id', None)
                request.session.pop('otp_expiry', None)

                messages.success(request, "Your account has been verified successfully.")
                return redirect('dashboard')
            except Account.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('register')
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, 'accounts/verify_otp.html')


def resend_register_otp(request):
    user_id = request.session.get('temp_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')

    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('register')

    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    cache.set(f"email_otp_{user.id}", otp, timeout=180)
    request.session['otp_expiry'] = int(time.time()) + 180

    # Send email
    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
    )

    mail_subject = 'Resend Account Verification OTP'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'activation_link': activation_link,
        'otp': otp,
    })
    EmailMessage(mail_subject, message, to=[user.email]).send()

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_otp')


# Authentication
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Collect variations
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    return redirect(params['next'])
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


# Dashboard & Profile
@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    return render(request, 'accounts/my_orders.html', {'orders': orders})


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter a valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order = Order.objects.get(order_number=order_id)
    subtotal = order.order_total - order.shipping_charge
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


# Password Reset with OTP
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            cache.set(f"reset_otp_{user.id}", otp, timeout=180)
            request.session['reset_user_id'] = user.id
            request.session['otp_expiry'] = int(time.time()) + 180

            # Send reset email
            reset_link = request.build_absolute_uri(
                reverse('resetpassword_validate', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
            )

            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'reset_link': reset_link,
                'otp': otp,
            })
            EmailMessage(mail_subject, message, to=[email]).send()

            messages.success(request, 'We sent you a reset password email with a link and OTP.')
            return redirect('verify_reset_otp')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def verify_reset_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('reset_user_id')

        if not user_id:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgotPassword')

        cached_otp = cache.get(f"reset_otp_{user_id}")
        if cached_otp and entered_otp == cached_otp:
            try:
                user = Account.objects.get(id=user_id)
                request.session['uid'] = user_id

                cache.delete(f"reset_otp_{user_id}")
                request.session.pop('reset_user_id', None)
                request.session.pop('otp_expiry', None)

                messages.success(request, "OTP verified. You can now reset your password.")
                return redirect('resetPassword')
            except Account.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('forgotPassword')
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
            return redirect('verify_reset_otp')

    return render(request, 'accounts/verify_reset_otp.html')


def resend_reset_otp(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please try again.")
        return redirect('forgotPassword')

    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('forgotPassword')

    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    cache.set(f"reset_otp_{user.id}", otp, timeout=180)
    request.session['otp_expiry'] = int(time.time()) + 180

    # Send email
    reset_link = request.build_absolute_uri(
        reverse('resetpassword_validate', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
    )

    mail_subject = 'Resend Reset Password OTP'
    message = render_to_string('accounts/reset_password_email.html', {
        'user': user,
        'reset_link': reset_link,
        'otp': otp,
    })
    EmailMessage(mail_subject, message, to=[user.email]).send()

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_reset_otp')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')
