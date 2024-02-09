from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed, name="feed"),
    path('user/posts/', views.user_posts, name='user_posts'),

    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='ticket_delete'),

    path('review/create/', views.review_and_ticket_create, name='review_and_ticket_create'),
    path('create-review/<int:ticket_id>/', views.create_review_from_ticket, name='create_review_from_ticket'),
    path('review/<int:review_id>/edit/', views.edit_review, name='review_edit'),
    path('review/<int:review_id>/delete/', views.delete_review, name='review_delete'),

    path('follow-users/', views.follow_users, name='follow_users'),
    path('unfollow-user/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('search-users/', views.search_users, name='search_users'),
]
