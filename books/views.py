from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout, login
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
import requests
import json
import os
from .models import Book, Shelf
from .forms import BookSearchForm, BookUploadForm, CustomUserCreationForm
from reviews.forms import ReviewForm


def index(request):
    """Home page view."""
    # Get recent user-uploaded books
    recent_books = Book.objects.filter(is_public=True, book_type='user_uploaded').order_by('-created_at')[:8]
    popular_books = Book.objects.filter(is_public=True, book_type='user_uploaded').order_by('-download_count')[:8]
    
    context = {
        'recent_books': recent_books,
        'popular_books': popular_books,
    }
    return render(request, 'books/index.html', context)


def book_detail(request, book_id):
    """Book detail page view."""
    try:
        # Try to get book from database by ID
        book = get_object_or_404(Book, id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return render(request, 'books/404.html')
    
    # Get user's review if logged in
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = book.reviews.get(user=request.user)
        except:
            pass
    
    # Get all reviews for this book
    reviews = book.reviews.all().order_by('-created_at')
    
    context = {
        'book': book,
        'user_review': user_review,
        'reviews': reviews,
        'review_form': ReviewForm(),
    }
    
    return render(request, 'books/book_detail.html', context)


def book_search(request):
    """Handle book search requests."""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            books = search_books_on_google(query)
            return render(request, 'books/search.html', {'books': books, 'query': query})
    
    return render(request, 'books/search.html')


def shelves(request):
    """User's bookshelves page."""
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view your bookshelves.")
        return render(request, 'books/shelves.html', {'shelves': []})
    
    # Get user's shelves
    shelves_data = {
        'currently_reading': Shelf.objects.filter(user=request.user, shelf_type='currently-reading'),
        'want_to_read': Shelf.objects.filter(user=request.user, shelf_type='want-to-read'),
        'read': Shelf.objects.filter(user=request.user, shelf_type='read'),
    }
    
    return render(request, 'books/shelves.html', {'shelves': shelves_data})


@login_required
@csrf_exempt
def add_to_shelf(request):
    """Add book to user's shelf."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            shelf_type = data.get('shelf_type')
            
            # Get or create book
            book = get_object_or_404(Book, id=book_id)
            
            # Create or update shelf entry
            shelf, created = Shelf.objects.get_or_create(
                user=request.user,
                book=book,
                shelf_type=shelf_type
            )
            
            if created:
                return JsonResponse({'success': True, 'message': f'Book added to {shelf_type.replace("-", " ")}'})
            else:
                return JsonResponse({'success': True, 'message': f'Book moved to {shelf_type.replace("-", " ")}'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def fetch_book_from_google(book_id):
    """Fetch book details from Google Books API."""
    try:
        url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching book: {e}")
    return None


def search_books_on_google(query, max_results=12):
    """Search books using Google Books API."""
    try:
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            'q': query,
            'maxResults': max_results
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
    except Exception as e:
        print(f"Error searching books: {e}")
    return []


def create_book_from_google_data(book_data):
    """Create Book instance from Google Books API data."""
    volume_info = book_data.get('volumeInfo', {})
    
    book, created = Book.objects.get_or_create(
        google_id=book_data.get('id'),
        defaults={
            'title': volume_info.get('title', ''),
            'authors': volume_info.get('authors', []),
            'description': volume_info.get('description', ''),
            'published_date': volume_info.get('publishedDate', ''),
            'page_count': volume_info.get('pageCount'),
            'categories': volume_info.get('categories', []),
            'average_rating': volume_info.get('averageRating'),
            'thumbnail_url': volume_info.get('imageLinks', {}).get('thumbnail', ''),
        }
    )
    
    return book


@login_required
def upload_book(request):
    """Upload a new book."""
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.book_type = 'user_uploaded'
            book.save()
            messages.success(request, f'Book "{book.title}" uploaded successfully!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookUploadForm()
    
    return render(request, 'books/upload_book.html', {'form': form})


def download_book(request, book_id):
    """Download a book file."""
    book = get_object_or_404(Book, id=book_id, is_public=True)
    
    if not book.book_file:
        raise Http404("Book file not available")
    
    # Increment download count
    book.increment_download_count()
    
    # Serve the file
    file_path = book.book_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{book.title}.{book.book_file.name.split(".")[-1]}"'
            return response
    else:
        raise Http404("Book file not found")


@login_required
def my_books(request):
    """User's uploaded books."""
    books = Book.objects.filter(uploaded_by=request.user).order_by('-created_at')
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    return render(request, 'books/my_books.html', {'books': books})


@login_required
def edit_book(request, book_id):
    """Edit a user's book."""
    book = get_object_or_404(Book, id=book_id, uploaded_by=request.user)
    
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookUploadForm(instance=book)
    
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, book_id):
    """Delete a user's book."""
    book = get_object_or_404(Book, id=book_id, uploaded_by=request.user)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('my_books')
    
    return render(request, 'books/delete_book.html', {'book': book})


def browse_books(request):
    """Browse all public books."""
    books = Book.objects.filter(is_public=True, book_type='user_uploaded').order_by('-created_at')
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        books = books.filter(categories__icontains=category)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        books = books.filter(
            models.Q(title__icontains=search_query) |
            models.Q(authors__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    # Get all categories for filter
    all_books = Book.objects.filter(is_public=True, book_type='user_uploaded')
    categories = []
    for book in all_books:
        categories.extend(book.categories)
    categories = list(set(categories))  # Remove duplicates
    
    context = {
        'books': books,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    }
    return render(request, 'books/browse_books.html', context)


@login_required
def user_profile(request):
    """User profile page."""
    # Get user's uploaded books
    uploaded_books = Book.objects.filter(uploaded_by=request.user).order_by('-created_at')
    
    # Get user's shelves
    shelves_data = {
        'currently_reading': Shelf.objects.filter(user=request.user, shelf_type='currently-reading'),
        'want_to_read': Shelf.objects.filter(user=request.user, shelf_type='want-to-read'),
        'read': Shelf.objects.filter(user=request.user, shelf_type='read'),
    }
    
    # Get user's reviews (if reviews app is working)
    user_reviews = []
    try:
        from reviews.models import Review
        user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')[:5]
    except:
        pass
    
    context = {
        'uploaded_books': uploaded_books,
        'shelves': shelves_data,
        'reviews': user_reviews,
    }
    return render(request, 'books/user_profile.html', context)


def signup(request):
    """Register a new user account."""
    if request.user.is_authenticated:
        return redirect('user_profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome to Novel Net, {user.username}! Your account has been created successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    """Log the user out and redirect to the home page."""
    try:
        auth_logout(request)
    finally:
        messages.success(request, 'You have been logged out.')
        return redirect('login')




@login_required
@staff_member_required
def users_report(request):
    """Staff-only report of users with login/activity info."""
    now = timezone.now()
    seven_days_ago = now - timezone.timedelta(days=7)

    users_qs = User.objects.all().order_by(models.F('last_login').desc(nulls_last=True), '-date_joined')

    total_users = users_qs.count()
    logged_in_count = users_qs.filter(last_login__isnull=False).count()
    joined_last_7_days = users_qs.filter(date_joined__gte=seven_days_ago).count()
    active_last_7_days = users_qs.filter(last_login__gte=seven_days_ago).count()

    context = {
        'users': users_qs,
        'total_users': total_users,
        'logged_in_count': logged_in_count,
        'joined_last_7_days': joined_last_7_days,
        'active_last_7_days': active_last_7_days,
    }
    return render(request, 'books/users_report.html', context)