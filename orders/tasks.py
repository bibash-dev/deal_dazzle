from django.core.mail import send_mail
from django.conf import settings
from django.db.models import ObjectDoesNotExist
from celery import shared_task
from smtplib import SMTPException
from .models import Order


@shared_task(name="orders.tasks.order_created", autoretry_for=(SMTPException,), retry_kwargs={'max_retries': 3},
             retry_backoff=True)
def order_created_email(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)

        subject = f'Order number: {order.id}'
        message = (
            f'Dear {order.first_name},\n\n'
            f'You have successfully placed an order.\n\n'
            f'Your order ID is {order.id}.'
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.email]

        mail_sent = send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        if mail_sent:
            return {"status": "success", "message": f"Email sent successfully to {order.email}."}
        else:
            return {"status": "error", "message": "Failed to send email."}

    except ObjectDoesNotExist:
        return {"status": "error", "message": f"Order with ID {order_id} does not exist."}
    except SMTPException as e:
        # Retry on SMTP-related errors
        raise e
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
