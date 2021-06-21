from django import forms
from .models import BillingInfo


class BillingInfoForm(forms.ModelForm):
    
    class Meta:
        model = BillingInfo
        exclude = ['session_order', 'order']
        widgets = {
            'address':forms.TextInput(attrs={'placeholder':'Street Address'}),
            'appartement':forms.TextInput(attrs={'placeholder':'Apartment. suite, unite ect ( optinal )'}),
            'account_password':forms.TextInput(attrs={'type':'password'}),
            'notes':forms.TextInput(attrs={'placeholder':'put some notes about your order'}),
            'create_account':forms.TextInput(attrs={'type':'checkbox', 'id':'acc'})
            # 'create_account':forms.BooleanField(required=False)
        }

    
class AccountForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type':'password'}))
        

 