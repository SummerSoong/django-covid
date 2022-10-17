from tkinter import Widget
from django import forms

class ContactForm(forms.Form):
	from_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "example@covid.com", "class": "form-control"}))
	subject = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "My subject", "class": "form-control"}))
	message = forms.CharField(required=True, widget=forms.Textarea(attrs={"placeholder": "My message", "class": "form-control"}))
