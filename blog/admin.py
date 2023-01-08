from django.contrib import admin
# each thing imported from models requires a separate class?
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

# this decorator registers both our post model and the post admin class with admin site
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')


@admin.register(Comment)
# inherits from admin.ModelAdmin which is a built-in django class
class CommentAdmin(admin.ModelAdmin):
# this class can access the fields created in the Comment class in models.py
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    # built-in feature of admin class. actions takes list of function names as argument
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
