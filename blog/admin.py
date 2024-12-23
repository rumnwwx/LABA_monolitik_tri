from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'avatar' )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'avatar')


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'published_at', 'likes')

