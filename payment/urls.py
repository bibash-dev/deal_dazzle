from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views, webhooks

app_name = 'payment'

urlpatterns = [
    # Payment process URLs
    path('process/', views.payment_process, name='process'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),

    # Stripe webhook URL (CSRF exempt)
    path('webhook/', csrf_exempt(webhooks.stripe_webhook), name='stripe_webhook'),
]