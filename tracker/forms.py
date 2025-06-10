from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from tracker.models import User, Profile, Transaction, MoneyTransfer


class UserCreationFormModfy(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    class Meta:
        model = User
        fields = ("first_name","last_name","email","password1","password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            return user

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['value_cad', 'value_usd', 'description', 'shop', 'transaction_type', 'category', 'payment_type',
                  'isd','tax_ec', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model = MoneyTransfer
        exclude = ['is_deleted','deleted_at']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }