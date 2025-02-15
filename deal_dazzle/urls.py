from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site
    path(f'{settings.ADMIN_URL}/', admin.site.urls),

    # Cart app
    path('cart/', include('cart.urls', namespace='cart')),

    # Orders app
    path('orders/', include('orders.urls', namespace='orders')),

    # Payment app
    path('payment/', include('payment.urls', namespace='payment')),

    # Coupons app
    path('coupons/', include('coupons.urls', namespace='coupons')),

    # Store app (main app)
    path('', include('store.urls', namespace='store')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
