from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module,Subscription


ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'description'], extra=2, can_delete=True)


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['your_email',]

"""
This is the ModuleFormSet formset. We build it using the inlineformset_factory()
function provided by Django. Inline formsets is a small abstraction on top of formsets
that simplifies working with related objects. This function allows us to build a model
formset dynamically for the Module objects related to a Course object.
We use the following parameters to build the formset:

• fields: The fields that will be included in each form of the formset.

• extra: Allows us to set up the number of empty extra forms to display in
the formset.

• can_delete: If you set this to True, Django will include a Boolean field for
each form that will be rendered as a checkbox input. It allows you to mark
the objects you want to delete.
"""