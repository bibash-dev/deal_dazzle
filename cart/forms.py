from django import forms


class CartAddProductForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

    quantity = forms.TypedChoiceField(
        choices=QUANTITY_CHOICES,
        coerce=int,
        label="Quantity",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput(),
        label="Override Quantity",
        help_text="Check this to replace the current quantity instead of adding to it.",
    )

    def __init__(self, *args, **kwargs):
        """
        Customize form initialization to dynamically set quantity choices if needed.
        """
        super().__init__(*args, **kwargs)

        # Example: Dynamically adjust quantity choices based on product stock
        if "max_quantity" in kwargs:
            max_quantity = kwargs.pop("max_quantity")
            self.fields["quantity"].choices = [(i, str(i)) for i in range(1, max_quantity + 1)]
