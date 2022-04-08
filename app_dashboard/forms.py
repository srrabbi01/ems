from django import forms
from django.forms import fields, widgets
from .models import *

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = [
            'name',
            'email',
            'phone',
            'location',
            ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-5'}),
            'phone': forms.TextInput(attrs={'class': 'input--style-5'}),
            'location': forms.TextInput(attrs={'class': 'input--style-5'}),
        }

class UserRegistrationUpdateForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = [
            'name',
            'email',
            'phone',
            'other_phone',
            'registration_type',
            'business_name',
            'post_office_or_union',
            'house_info',
            'nid',
            'picture',
            'location',
            ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-5'}),
            'phone': forms.TextInput(attrs={'class': 'input--style-5'}),
            'other_phone': forms.TextInput(attrs={'class': 'input--style-5'}),
            'registration_type': forms.Select(attrs={'class': 'reg_type'}),
            'business_name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'post_office_or_union': forms.TextInput(attrs={'class': 'input--style-5'}),
            'house_info': forms.TextInput(attrs={'class': 'input--style-5'}),
            'nid': forms.TextInput(attrs={'class': 'input--style-5'}),
            'location': forms.TextInput(attrs={'class': 'input--style-5'}),
        }

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'details', 'service_category', 'priority', 'files']

        widgets = {
                'title': forms.TextInput(attrs={'class': 'input--style-5'}),
                'details': forms.Textarea(attrs={'class': 'input--style-5', 'rows': '4', 'cols': '40'}),
                'service_category': forms.Select(attrs={'class': 'priority-select'}),
                'priority': forms.Select(attrs={'class': 'priority-select'}),
                'files': forms.FileInput(attrs={'accept': '.pdf, .jpg, .jpeg, .png, .doc, .docx, .xls, .xlsx, .txt'}),
            }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['details', 'equip_charge', 'files']

        widgets = {
                'details': forms.Textarea(attrs={'class': 'input--style-5', 'rows': '4', 'placeholder': 'Write about equivment/parts details...'}),
                'equip_charge': forms.NumberInput(attrs={'class': 'input--style-5', 'placeholder': 'Enter equipment/parts charge...'}),
                'files': forms.FileInput(attrs={'accept': '.pdf, .jpg, .jpeg, .png, .doc, .docx, .xls, .xlsx, .txt'}),
            }

class CustomerPaymentForm(forms.ModelForm):
    class Meta:
        model = CustomerPayment
        fields = ('transition_id','payment_method','payment_date')
        widgets = {
            'transition_id':forms.TextInput(attrs={'class': 'input--style-5', 'placeholder': 'Enter transition id'}),
            'payment_method':forms.TextInput(attrs={'class': 'input--style-5', 'placeholder': 'Enter payment method'}),
            'payment_date':forms.DateInput(attrs={'class': 'input--style-5', 'placeholder': 'Enter payment date','type':'date'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','desc']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'desc': forms.Textarea(attrs={'class': 'form-control','cols':'40','rows':'5','placeholder': 'Description'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
                'comment': forms.Textarea(attrs={'class': 'input--style-5', 'rows': '4', 'placeholder': 'Write your comments...'}),  
    }