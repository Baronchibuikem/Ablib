from django import forms

class ContactForm(forms.Form):
    Your_name = forms.CharField(max_length= 100)
    Message = forms.CharField(widget=forms.Textarea)
    Your_email = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
