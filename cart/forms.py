from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CartAddProductForm(forms.Form):
    """ Form for adding a product to the cart. """
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
        widget=forms.HiddenInput(),
        label="Override Quantity",
        help_text="Check this to replace the current quantity instead of adding to it.",
    )

    def __init__(self, *args, **kwargs):
        """ Customize form initialization to dynamically set quantity validators and choices. """
        self.max_quantity = kwargs.pop("max_quantity", None)
        super().__init__(*args, **kwargs)

        # Dynamically adjust the max value for quantity based on product stock
        if self.max_quantity is not None:
            self.fields["quantity"].validators.append(MaxValueValidator(self.max_quantity))
            self.fields["quantity"].widget.attrs["max"] = self.max_quantity

    def clean(self):
        """ Custom validation to ensure the quantity does not exceed the available stock. """
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        max_quantity = self.max_quantity

        if max_quantity is not None and quantity > max_quantity:
            raise forms.ValidationError(
                f"Quantity cannot exceed available stock ({max_quantity})."
            )

        return cleaned_data
