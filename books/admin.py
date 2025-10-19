from django.contrib import admin
from .models import Book, Shelf, UserProfile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_names', 'published_date', 'average_rating', 'created_at']
    list_filter = ['created_at', 'published_date', 'average_rating']
    search_fields = ['title', 'authors']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'shelf_type', 'added_at']
    list_filter = ['shelf_type', 'added_at']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['added_at', 'updated_at']
    ordering = ['-added_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'location']
    readonly_fields = ['created_at', 'updated_at']
