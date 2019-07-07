from django import forms
from phonenumber_field.formfields import PhoneNumberField
from allauth.account.forms import SignupForm
from django.http.request import QueryDict

from .models import Order, Category


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'address',
        

class CategoryForm(forms.Form):
    OPTIONS = Category.objects.all().values_list('id', 'name')

    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=OPTIONS,
        label='Categories:',
        initial=Category.objects.all().values_list('id', flat=True),
    )


class StoreSignupForm(SignupForm):
    email = forms.EmailField(max_length=35, label='email')
    name = forms.CharField(max_length=50, label='Full Name')
    phone = PhoneNumberField()

    def save(self, request):
        user = super(StoreSignupForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.save()

        return user
