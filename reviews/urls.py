from django.urls import path
from . import views

urlpatterns = [
    path('submit/<str:book_id>/', views.submit_review, name='submit_review'),
    path('submit-ajax/', views.submit_review_ajax, name='submit_review_ajax'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
