from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class BookClub(models.Model):
    """Model representing a book club."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clubs')
    members = models.ManyToManyField(User, related_name='book_clubs', through='ClubMembership')
    current_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_clubs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()


class ClubMembership(models.Model):
    """Model representing membership in a book club."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'club']
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} in {self.club.name}"


class ClubDiscussion(models.Model):
    """Model representing discussions within a book club."""
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='discussions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} in {self.club.name}"
