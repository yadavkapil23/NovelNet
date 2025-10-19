from django.contrib import admin
from .models import Review, BookRating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'book__title', 'review_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
