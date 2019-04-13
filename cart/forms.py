from django import forms
PRODUCT_QUALITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """ add products to the cart"""
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUALITY_CHOICES)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
