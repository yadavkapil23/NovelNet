from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    """Model representing a book - can be user-uploaded or from external sources."""
    BOOK_TYPES = [
        ('user_uploaded', 'User Uploaded'),
        ('external', 'External Source'),
    ]
    
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES, default='user_uploaded')
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    title = models.CharField(max_length=500)
    authors = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    categories = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True, blank=True
    )
    thumbnail_url = models.URLField(max_length=1000, blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    book_file = models.FileField(upload_to='book_files/', null=True, blank=True, help_text="PDF, EPUB, or other book format")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_books', null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="Whether this book is visible to all users")
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def author_names(self):
        """Return authors as a comma-separated string."""
        if self.authors:
            # If it's already a comma-separated string, return it
            if isinstance(self.authors, str):
                return self.authors
            # If it's a list, join it
            elif isinstance(self.authors, list):
                return ', '.join(self.authors)
        return 'Unknown Author'
    
    @property
    def cover_image_url(self):
        """Return the cover image URL (uploaded or external)."""
        if self.cover_image:
            return self.cover_image.url
        elif self.thumbnail_url:
            return self.thumbnail_url
        return None
    
    def increment_download_count(self):
        """Increment the download count."""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Shelf(models.Model):
    """Model representing a user's bookshelf."""
    SHELF_TYPES = [
        ('currently-reading', 'Currently Reading'),
        ('want-to-read', 'Want to Read'),
        ('read', 'Read'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelves')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='shelf_entries')
    shelf_type = models.CharField(max_length=20, choices=SHELF_TYPES)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'book', 'shelf_type']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.shelf_type})"


class UserProfile(models.Model):
    """Extended user profile for additional user information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class EmailVerification(models.Model):
    """Model for storing email verification OTPs."""
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.email}"
    
    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP."""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Check if OTP has expired."""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is valid and not expired."""
        return not self.is_expired() and not self.is_verified
