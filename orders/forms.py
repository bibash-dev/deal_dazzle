from django import forms
from django.core.validators import EmailValidator, RegexValidator
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'postal_code',
            'city',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'address': 'Shipping Address',
            'postal_code': 'Postal Code',
            'city': 'City',
        }
        help_texts = {
            'email': 'We’ll never share your email with anyone else.',
            'postal_code': 'Enter a valid postal code (e.g., 12345 or A1B 2C3).',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validator = EmailValidator(message="Please enter a valid email address.")
        validator(email)
        return email

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        us_zip_validator = RegexValidator(
            regex=r'^\d{5}(?:[-\s]\d{4})?$',
            message="Enter a valid US ZIP code (e.g., 12345 or 12345-6789).",
        )
        canada_postal_validator = RegexValidator(
            regex=r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$',
            message="Enter a valid Canadian postal code (e.g., A1B 2C3).",
        )
        try:
            us_zip_validator(postal_code)
        except:
            try:
                canada_postal_validator(postal_code)
            except:
                raise forms.ValidationError("Enter a valid postal code.")
        return postal_code
