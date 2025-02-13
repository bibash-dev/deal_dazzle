from celery import shared_task
from django.core.mail import send_mail
from django.db.models import ObjectDoesNotExist
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)

        subject = f'Order number: {order.id}'
        message = f'Dear {order.first_name},\n\nYou have successfully placed an order.'
        from_email = 'admin@dealdazzle.com'
        recipient_list = [order.email]

        mail_sent = send_mail(subject, message, from_email, recipient_list)
        if mail_sent:
            return {"status": "success", "message": "Email sent successfully."}
        else:
            return {"status": "error", "message": "Failed to send email."}

    except ObjectDoesNotExist:
        return {"status": "error", "message": f"Order with ID {order_id} does not exist."}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
