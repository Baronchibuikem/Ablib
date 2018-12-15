from django.contrib import admin
from .models import Post, Comment
from pagedown.widgets import AdminPagedownWidget
from django.db import models


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created',)
    list_filter = ('created', 'updated')
    search_fields = ('name', 'body')

admin.site.register(Comment, CommentAdmin)

