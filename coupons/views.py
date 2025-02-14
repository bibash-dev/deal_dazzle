from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import ApplyCouponForm
from .models import Coupon


@require_POST
def apply_coupon(request):
    now = timezone.now()
    form = ApplyCouponForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = get_object_or_404(
                Coupon,
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
            messages.success(request, 'Coupon applied successfully!')
        except Coupon.DoesNotExist:
            if 'coupon_id' in request.session:
                request.session.pop('coupon_id')
            messages.error(request, 'Invalid or expired coupon.')

    return redirect(reverse('cart:cart_detail'))
