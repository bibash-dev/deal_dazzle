from io import BytesIO
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification with an invoice when an order is successfully paid.
    """
    try:
        order = Order.objects.get(id=order_id)

        # Prepare email subject and message
        subject = f'Deal Dazzle - Invoice no. {order.id}'
        message = 'Please, find attached the invoice for your recent purchase.'

        # Create the email object
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='admin@dealdazzle.com',
            to=[order.email],
        )

        # Render the HTML template for the PDF
        html = render_to_string('admin/orders/order/pdf.html', {'order': order})

        # Generate the PDF
        out = BytesIO()
        HTML(string=html).write_pdf(out)

        # Attach the PDF to the email
        email.attach(
            filename=f'order_{order.id}.pdf',
            content=out.getvalue(),
            mimetype='application/pdf',
        )

        # Send the email
        email.send()

    except Order.DoesNotExist:
        print(f"Error: Order with id {order_id} does not exist.")
    except Exception as e:
        print(f"Error: Failed to send invoice email for order {order_id}. Error: {str(e)}")
