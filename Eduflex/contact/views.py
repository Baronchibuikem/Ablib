from django.core.mail import send_mail
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def contact(request):
    form = ContactForm()
    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']
        recipients = ['baronchibuike@gmail.com']
        if cc_myself:
            recipients.append(sender)
        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect()
    context = {'form': form}
    return render(request, 'contact/contact.html',context)

