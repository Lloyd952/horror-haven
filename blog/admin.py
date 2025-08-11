from django.contrib import admin
from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['film_title', 'year', 'director', 'rating', 'author', 'status', 'created_on']
    list_filter = ['status', 'rating', 'created_on', 'year']
    search_fields = ['film_title', 'director', 'body']
    prepopulated_fields = {'slug': ('film_title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_on'
    ordering = ['status', '-created_on']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_on', 'is_active']
    list_filter = ['is_active', 'created_on']
    search_fields = ['user', 'body']
    raw_id_fields = ['user', 'post']
