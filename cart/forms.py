from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label="Quantity",
        validators=[
            MinValueValidator(1, message="Quantity must be at least 1."),
            MaxValueValidator(20, message="Quantity cannot exceed 20."),
        ],
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 20}),
        initial=1,
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
        label="Override Quantity",
        help_text="Check this to replace the current quantity instead of adding to it.",
    )
