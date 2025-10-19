from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.book_search, name='book_search'),
    path('shelves/', views.shelves, name='shelves'),
    path('add-to-shelf/', views.add_to_shelf, name='add_to_shelf'),
    path('upload/', views.upload_book, name='upload_book'),
    path('browse/', views.browse_books, name='browse_books'),
    path('my-books/', views.my_books, name='my_books'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('book/<int:book_id>/download/', views.download_book, name='download_book'),
]
