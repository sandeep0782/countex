from django import forms
from django.contrib.auth.models import User
from .models import *




class SamplingForm(forms.ModelForm):
    class Meta:
        model=Sampling
        fields=['design_name','product','color_name','buyer','supplier','season','drop','technique','dos','image']
        

class SeasonForm(forms.ModelForm):
    class Meta:
        model=Season
        fields='__all__'

class DropForm(forms.ModelForm):
    class Meta:
        model=Drop
        fields='__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields='__all__'

class BuyerForm(forms.ModelForm):
    class Meta:
        model=Buyer
        fields='__all__'
        
class Bulk_UpdateForm(forms.ModelForm):
    class Meta:
        model=Bulk_Order
        fields='__all__'