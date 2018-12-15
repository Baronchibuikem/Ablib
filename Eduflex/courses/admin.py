from django.contrib import admin
from .models import Subject, Course, Module, Subscription
from django.db import models
from pagedown.widgets import AdminPagedownWidget

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug':('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField:{'widget': AdminPagedownWidget}}
    list_display = ['title', 'subject', 'created', 'image']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug':('title',)}
    inlines = [ModuleInline]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['your_email']
admin.site.register(Subscription, SubscriptionAdmin)

"""
The models for the course application are now registered in the administration site.
We use the @admin.register() decorator instead of the admin.site.register() function. Both provide the same functionality.
"""