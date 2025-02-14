from django import forms


class ApplyCouponForm(forms.Form):
    code = forms.CharField(
        label="Coupon Code",
        widget=forms.TextInput(attrs={'placeholder': 'Enter coupon code'}),
    )
