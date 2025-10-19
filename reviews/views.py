from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Review, BookRating
from .forms import ReviewForm
from books.models import Book


@login_required
def submit_review(request, book_id):
    """Submit a book review."""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.get_or_create(
                user=request.user,
                book=book,
                defaults=form.cleaned_data
            )
            
            if not created:
                # Update existing review
                review.rating = form.cleaned_data['rating']
                review.review_text = form.cleaned_data['review_text']
                review.save()
                messages.success(request, "Review updated successfully!")
            else:
                messages.success(request, "Review submitted successfully!")
            
            return redirect('book_detail', book_id=book_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {
        'form': form,
        'book': book
    })


@login_required
@csrf_exempt
def submit_review_ajax(request):
    """Submit review via AJAX."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            rating = data.get('rating')
            review_text = data.get('review_text', '')
            
            book = get_object_or_404(Book, id=book_id)
            
            review, created = Review.objects.get_or_create(
                user=request.user,
                book=book,
                defaults={
                    'rating': rating,
                    'review_text': review_text
                }
            )
            
            if not created:
                review.rating = rating
                review.review_text = review_text
                review.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Review submitted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    })


@login_required
def delete_review(request, review_id):
    """Delete a user's review."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('book_detail', book_id=book_id)
