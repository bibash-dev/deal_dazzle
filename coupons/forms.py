from django import forms


class ApplyCouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter coupon code'}),
    )
