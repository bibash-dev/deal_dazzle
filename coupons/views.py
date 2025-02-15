from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import ApplyCouponForm
from .models import Coupon


@require_POST
def apply_coupon(request):
    """ Apply a coupon to the user's cart. """
    form = ApplyCouponForm(request.POST)

    if not form.is_valid():
        messages.error(request, 'Invalid form submission.')
        return redirect(reverse('cart:cart_detail'))

    code = form.cleaned_data['code']
    now = timezone.now()

    try:
        coupon = Coupon.objects.get(code__iexact=code)
        if coupon.is_valid():
            request.session['coupon_id'] = coupon.id
            messages.success(request, 'Coupon applied successfully!')
        else:
            if coupon.valid_to < now:
                messages.error(request, 'This coupon has expired.')
            elif not coupon.active:
                messages.error(request, 'This coupon is not active.')
            request.session['coupon_id'] = None
    except Coupon.DoesNotExist:
        messages.error(request, 'Invalid coupon code.')
        request.session['coupon_id'] = None

    return redirect(reverse('cart:cart_detail'))
