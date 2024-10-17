# admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, Category  # Import Category here
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Profile
from .models import Subscriber

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'bio')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('user',)  # Make the user field read-only

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new profile
            obj.user = request.user
        super().save_model(request, obj, form, change)
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'trending', 'description', 'slug')
    list_filter = ('author', 'category', 'trending')
    search_fields = ('title', 'content', 'description', 'slug')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('post', 'author')
    search_fields = ('content',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
