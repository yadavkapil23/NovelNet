from django.urls import path
from . import views

urlpatterns = [
    path('', views.clubs_list, name='clubs_list'),
    path('create/', views.create_club, name='create_club'),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
    path('<int:club_id>/join/', views.join_club, name='join_club'),
    path('<int:club_id>/leave/', views.leave_club, name='leave_club'),
    path('<int:club_id>/discussion/create/', views.create_discussion, name='create_discussion'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
]
