from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, EmailVerification
from django.core.exceptions import ValidationError


class BookSearchForm(forms.Form):
    """Form for searching books."""
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or ISBN...',
            'required': True
        })
    )


class BookUploadForm(forms.ModelForm):
    """Form for uploading books."""
    class Meta:
        model = Book
        fields = ['title', 'authors', 'description', 'published_date', 'page_count', 'categories', 'cover_image', 'book_file', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title...'
            }),
            'authors': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter authors separated by commas (e.g., John Doe, Jane Smith)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter book description...'
            }),
            'published_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
            'page_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of pages'
            }),
            'categories': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter categories separated by commas (e.g., Fiction, Romance, Mystery)'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'book_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.epub,.mobi,.txt'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].required = False
        self.fields['description'].required = False
        self.fields['published_date'].required = False
        self.fields['page_count'].required = False
        self.fields['categories'].required = False
        self.fields['cover_image'].required = False
        self.fields['book_file'].required = False

    def clean_authors(self):
        """Clean authors field - keep as comma-separated string."""
        authors = self.cleaned_data.get('authors', '')
        if authors:
            # Clean up the string - remove extra spaces and normalize
            authors_list = [author.strip() for author in authors.split(',') if author.strip()]
            return ', '.join(authors_list)
        return ''

    def clean_categories(self):
        """Clean categories field - keep as comma-separated string."""
        categories = self.cleaned_data.get('categories', '')
        if categories:
            # Clean up the string - remove extra spaces and normalize
            categories_list = [category.strip() for category in categories.split(',') if category.strip()]
            return ', '.join(categories_list)
        return ''


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with optional email field."""
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address (optional)'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def clean_email(self):
        """Validate email uniqueness if provided; allow blank emails."""
        email = self.cleaned_data.get('email')
        if not email:
            return ''
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class EmailVerificationForm(forms.Form):
    """Form for email verification with OTP."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    def clean_email(self):
        """Validate email and check if user already exists."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class OTPVerificationForm(forms.Form):
    """Form for OTP verification."""
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter 6-digit OTP',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        })
    )
    
    def clean_otp(self):
        """Validate OTP format."""
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError("OTP must be a 6-digit number.")
        return otp
