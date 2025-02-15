# Deal Dazzle - Online Store

Deal Dazzle is a Django powered online store. It provides a seamless shopping experience for customers, allowing them to browse products, add items to their cart, apply discount codes, complete the checkout process, and pay securely using a credit card. The project also includes a recommendation engine to suggest products to customers, enhancing their shopping experience.

## Features

- **Product Browsing**: Customers can browse through a wide range of products.
- **Shopping Cart**: Add products to the cart and manage quantities.
- **Coupon Codes**: Apply discount codes during checkout.
- **Checkout Process**: Secure and user-friendly checkout process.
- **Payment Gateway**: Integrated Stripe payment gateway for secure credit card payments.
- **PDF Invoices**: Dynamically generate PDF invoices for completed orders.
- **Recommendation Engine**: Built-in product recommendation engine using Redis.
- **Coupon System**: Create and manage discount coupons.
- **Asynchronous Notifications**: Configured Celery with RabbitMQ to send asynchronous email notifications for order creation and PDF generation of order details.

## Technologies Used

- **Django**: The core framework used to build the online store.
- **Celery**: Handles asynchronous tasks such as sending emails and generating PDFs.
- **RabbitMQ**: Message broker for Celery.
- **Stripe**: Payment gateway for processing credit card payments.
- **Redis**: Used for the product recommendation engine.
- **WeasyPrint**: For generating PDF invoices.

## Installation

To get started with Deal Dazzle, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bibash-dev/deal-dazzle.git
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   SECRET_KEY=your_secret_key
   DEBUG=True
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   DATABASE_URL=your_database_url
   REDIS_URL=your_redis_url
   EMAIL_HOST=your_email_host
   EMAIL_PORT=your_email_port
   EMAIL_HOST_USER=your_email_user
   EMAIL_HOST_PASSWORD=your_email_password
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Start Celery Worker**:
   ```bash
   celery -A deal_dazzle worker -l info
   ```

8. **Start RabbitMQ**:
   Ensure RabbitMQ is installed and running on your system.

## Configuration

### Stripe Integration
To process payments, you need to set up Stripe. Add your Stripe secret and public keys to the `.env` file.

### Redis Configuration
Redis is used for the product recommendation engine. Ensure Redis is installed and running, and add the Redis URL to the `.env` file.

### Email Configuration
Configure the email settings in the `.env` file to send asynchronous notifications to customers.

## Usage

### Admin Panel
Access the admin panel at `/admin` to manage products, orders, coupons, and more.

### Product Recommendation Engine
The recommendation engine suggests products to customers based on items that are frequently purchased together. This is powered by Redis.

### Coupon System
Create and manage discount coupons from the admin panel. Customers can apply these coupons during checkout.

### PDF Invoices
PDF invoices are generated dynamically and sent to customers via email after a successful purchase.

## Acknowledgments

- Django Documentation
- Stripe API Documentation
- Celery Documentation
- Redis Documentation

---

**Deal Dazzle** - Your one-stop online shopping destination! 🛒✨