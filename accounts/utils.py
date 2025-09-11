import random
from django.core.cache import cache

def generate_otp(user_id, validity=300, resend_block=120):
    """
    Generate a new OTP for user, valid for `validity` seconds,
    and block resends for `resend_block` seconds.
    """
    otp = str(random.randint(100000, 999999))

    # Store OTP (expires in 5 min by default)
    cache.set(f"otp_{user_id}", otp, timeout=validity)

    # Block resends (expires in 2 min by default)
    cache.set(f"otp_resend_block_{user_id}", True, timeout=resend_block)

    return otp

def can_resend_otp(user_id):
    """
    Check if resend is allowed (no block key in cache).
    """
    return not cache.get(f"otp_resend_block_{user_id}")
