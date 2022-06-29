from django.contrib import admin
from .models import Post, Profile, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'body', 'publish')
    list_filter = ('author', 'publish')
    search_fields = ('title', 'author', 'body')
    raw_id_fields = ('author',)


admin.site.register(Profile)
admin.site.register(Follow)
