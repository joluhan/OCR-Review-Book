from django.urls import path
from . import views  # Import views from the current package

# Define urlpatterns list to hold all URL configurations for the app
urlpatterns = [
    # URL for the feed view. This will match the URL '/feed/' and route it to views.feed.
    path('feed/', views.feed, name="feed"),
    
    # URL for listing user posts. Matches '/user/posts/' and routes to views.user_posts.
    path('user/posts/', views.user_posts, name='user_posts'),

    # URLs for ticket-related actions: creating, editing, and deleting tickets.
    # Create ticket: Matches '/ticket/create/' and routes to views.ticket_create.
    path('ticket/create/', views.ticket_create, name='ticket_create'),
    # Edit ticket: Uses a dynamic segment <int:ticket_id> to capture the ticket ID.
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='ticket_edit'),
    # Delete ticket: Also uses <int:ticket_id> for specifying which ticket to delete.
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='ticket_delete'),

    # URLs for review-related actions: creating a review with or without a ticket, editing, and deleting reviews.
    # Create review and ticket together: This might be used for a form that submits both a ticket and a review.
    path('review/create/', views.review_and_ticket_create, name='review_and_ticket_create'),
    # Create review for an existing ticket: Uses <int:ticket_id> to specify the ticket.
    path('create-review/<int:ticket_id>/', views.create_review_from_ticket, name='create_review_from_ticket'),
    # Edit review: Uses <int:review_id> to capture the review ID for editing.
    path('review/<int:review_id>/edit/', views.edit_review, name='review_edit'),
    # Delete review: Uses <int:review_id> for specifying which review to delete.
    path('review/<int:review_id>/delete/', views.delete_review, name='review_delete'),

    # URLs for following and unfollowing users, and searching for users.
    # Follow users: Matches '/follow-users/' and routes to views.follow_users.
    path('follow-users/', views.follow_users, name='follow_users'),
    # Unfollow user: Uses <int:user_id> to specify which user to unfollow.
    path('unfollow-user/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    # Search for users: Matches '/search-users/' and routes to views.search_users.
    path('search-users/', views.search_users, name='search_users'),
]
