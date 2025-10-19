from django.contrib import admin
from .models import BookClub, ClubMembership, ClubDiscussion


@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'club', 'is_admin', 'joined_at']
    list_filter = ['is_admin', 'joined_at']
    search_fields = ['user__username', 'club__name']
    readonly_fields = ['joined_at']
    ordering = ['-joined_at']


@admin.register(ClubDiscussion)
class ClubDiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'user', 'created_at']
    list_filter = ['created_at', 'club']
    search_fields = ['title', 'content', 'user__username', 'club__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
