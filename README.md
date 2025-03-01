# **Deal Dazzle - Online Store**

**Deal Dazzle** is a **Django-powered online store** designed to provide a seamless and engaging shopping experience. Customers can browse products, manage their shopping cart, apply discount codes, and complete secure payments using **Stripe**. The platform also features a **product recommendation engine** powered by **Redis**, **PDF invoice generation**, and **asynchronous email notifications** using **Celery** and **RabbitMQ**.

---

## **Features**

### **Product Browsing**
- Browse a wide range of products with detailed descriptions and images.
- Filter and search products by category, price, or popularity.

### **Shopping Cart**
- Add products to the cart and adjust quantities.
- View cart summary with total price and applied discounts.

### **Coupon System**
- Apply discount codes during checkout.
- Admin panel to create, manage, and track coupon usage.

### **Secure Checkout**
- User-friendly checkout process with multiple payment options.
- Integrated **Stripe** payment gateway for secure credit card payments.

### **PDF Invoices**
- Automatically generate and email PDF invoices for completed orders.
- Built using **WeasyPrint** for professional and customizable invoices.

### **Product Recommendations**
- Suggest products to customers based on frequently purchased items.
- Powered by **Redis** for fast and efficient recommendations.

### **Asynchronous Notifications**
- Send email notifications for order confirmations and invoice generation.
- Configured with **Celery** and **RabbitMQ** for reliable and scalable task processing.

### **Admin Panel**
- Manage products, orders, coupons, and customer data from a centralized admin interface.

---

## **Technologies Used**

- **Backend Framework**: Django
- **Asynchronous Task Queue**: Celery
- **Message Broker**: RabbitMQ
- **Payment Gateway**: Stripe
- **Recommendation Engine**: Redis
- **PDF Generation**: WeasyPrint
- **Database**: Any Django-supported database
- **Email Service**: SMTP (configurable with any email provider)

---

## **Installation**

### **Prerequisites**

- Python 3.9 or higher
- A Django-supported database
- Redis (for the recommendation engine)
- RabbitMQ (for Celery)
- Stripe account (for payment processing)

### **Steps**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bibash-dev/deal-dazzle.git
   cd deal-dazzle
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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
   DATABASE_URL=your_database_url
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLIC_KEY=your_stripe_public_key
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

---

## **Configuration**

### **Stripe Integration**
- Add your **Stripe Secret Key** and **Stripe Public Key** to the `.env` file.
- Configure webhooks in the Stripe dashboard to handle payment events.

### **Redis Configuration**
- Install and run Redis on your system.
- Add the Redis URL to the `.env` file for the recommendation engine.

### **Email Configuration**
- Configure SMTP settings in the `.env` file to enable email notifications.
- Supported email providers: Gmail, SendGrid, Amazon SES, etc.

---

## **Usage**

### **Admin Panel**
- Access the admin panel at `/admin` to manage:
  - Products (add, edit, delete)
  - Orders (view, update status)
  - Coupons (create, manage, track usage)
  - Customer data (view, manage)

### **Product Recommendation Engine**
- The recommendation engine suggests products based on frequently purchased items.
- Powered by **Redis** for fast and efficient recommendations.

### **Coupon System**
- Create and manage discount coupons from the admin panel.
- Customers can apply coupons during checkout to receive discounts.

### **PDF Invoices**
- PDF invoices are automatically generated and emailed to customers after a successful purchase.
- Customize invoice templates using Django templates and **WeasyPrint**.

### **Asynchronous Notifications**
- Email notifications are sent asynchronously for:
  - Order confirmations
  - Invoice generation
- Configured with **Celery** and **RabbitMQ** for reliable task processing.

---

---

## **Acknowledgments**

- **Django Documentation**: For building a robust and scalable backend.
- **Stripe API Documentation**: For seamless payment integration.
- **Celery Documentation**: For handling asynchronous tasks.
- **Redis Documentation**: For powering the recommendation engine.
- **WeasyPrint Documentation**: For generating professional PDF invoices.

---

**Deal Dazzle** - Your one-stop online shopping destination! 🛒✨

---
