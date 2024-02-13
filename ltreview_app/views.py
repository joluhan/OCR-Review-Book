from itertools import chain
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models import User
from .models import Ticket
from .models import Review
from .forms import ReviewForm, SearchUsersForm, TicketForm

@login_required  # Ensure only logged-in users can access this view
def feed(request):
    # Get the current logged-in user
    user = request.user

    # Retrieve all tickets created by the user
    user_tickets = Ticket.objects.filter(user=user)

    # Retrieve all reviews authored by the user
    user_reviews = Review.objects.filter(author=user)

    # Retrieve all reviews on the user's tickets, excluding those authored by the user
    ticket_reviews = list(chain(*[ticket.review_set.all().exclude(author=user) for ticket in user_tickets]))

    # Retrieve tickets from users the current user is following
    followed_user_tickets = Ticket.objects.filter(user__in=user.follows.all())

    # Retrieve reviews on tickets from followed users or by followed users, excluding the current user's reviews
    followed_user_reviews = Review.objects.filter(
        Q(contributors__in=user.follows.all()) | Q(ticket__in=followed_user_tickets)
    ).exclude(author=user)

    # Initialize a list to keep track of tickets the user has reviewed
    user_has_created_review = []

    # Check each followed user's ticket to see if the current user has left a review
    for ticket in followed_user_tickets:
        if Review.objects.filter(ticket=ticket, author=user).exists():
            user_has_created_review.append(ticket.id)  # Add ticket ID to list if user has reviewed it

    # Combine all relevant tickets and reviews into a single list and sort by creation time, newest first
    reviews_and_tickets = sorted(
        chain(user_tickets, user_reviews, followed_user_tickets, followed_user_reviews, ticket_reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    # Prepare the context with the combined list and the list of reviewed tickets by the user
    context = {
        'reviews_and_tickets': reviews_and_tickets,
        'user_has_created_review': user_has_created_review,
    }

    # Render the feed page with the context
    return render(request, 'ltreview/feed.html', context=context)

@login_required  # Ensures that only authenticated users can access this view
def ticket_create(request):
    # Initialize an empty ticket form
    ticket_form = TicketForm()

    # Check if the form was submitted
    if request.method == 'POST':
        # Populate the form with data from the request
        ticket_form = TicketForm(request.POST, request.FILES)
        
        # Check if the form is valid (all required fields are filled and valid)
        if ticket_form.is_valid():
            # Save the form to create a Ticket instance, but don't commit to the database yet
            ticket = ticket_form.save(commit=False)
            # Assign the current user as the ticket's user
            ticket.user = request.user
            # Save the Ticket instance to the database
            ticket.save()
            # Redirect the user to the feed page after successful submission
            return redirect('feed')
    
    # If the request method is not POST, or the form is not valid, render the page with the form
    return render(request, 'ltreview/ticket_create.html', context={'ticket_form': ticket_form})

@login_required  # Ensures that only authenticated users can access this view
def create_review_from_ticket(request, ticket_id):
    # Retrieve the ticket by ID or return a 404 error if it doesn't exist
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Initialize an empty review form
    review_form = ReviewForm()

    # Check if the form was submitted
    if request.method == 'POST':
        # Populate the form with data from the request
        review_form = ReviewForm(request.POST)
        
        # Check if the form is valid
        if review_form.is_valid():
            # Save the form to create a Review instance, but don't commit to the database yet
            review = review_form.save(commit=False)
            # Assign the current user as the review's author
            review.author = request.user
            # Link the review to the specified ticket
            review.ticket = ticket
            # Save the Review instance to the database
            review.save()
            # Optionally, add the current user as a contributor to the review
            review.contributors.add(request.user, through_defaults={'contribution': 'Main author'})
            # Redirect the user to the feed page after successful submission
            return redirect('feed')

    # Prepare the context with the review form and ticket instance
    context = {
        'review_form': review_form,
        'ticket': ticket,
    }
    
    # If the request method is not POST, or the form is not valid, render the page with the form and ticket details
    return render(request, 'ltreview/create_review_from_ticket.html', context=context)

@login_required  # Ensures that only authenticated users can access this function
def review_and_ticket_create(request):
    # Initialize the forms with no initial data
    review_form = ReviewForm()
    ticket_form = TicketForm()

    # Check if the user submitted the form (POST request)
    if request.method == 'POST':
        # Populate the forms with data from the request
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)

        # Initialize a variable to None for the ticket. It will be used to associate the review with the ticket if valid.
        ticket = None

        # Validate the ticket form
        if ticket_form.is_valid():
            # Save the ticket form data to create a Ticket instance but don't commit to the database yet
            ticket = ticket_form.save(commit=False)
            # Set the current user as the ticket's user
            ticket.user = request.user
            # Save the Ticket instance to the database
            ticket.save()

        # Validate the review form
        if review_form.is_valid():
            # Save the review form data to create a Review instance but don't commit to the database yet
            review = review_form.save(commit=False)
            # Set the current user as the review's author
            review.author = request.user
            # Associate the review with the previously saved ticket
            review.ticket = ticket
            # Save the Review instance to the database
            review.save()
            # Add the current user as a contributor to the review with a specific role
            review.contributors.add(request.user, through_defaults={'contribution': 'Main author'})
        
        # After saving both the ticket and review, redirect the user to the feed page
        return redirect('feed')

    # If the request method is not POST, or after the forms are initialized (GET request), prepare the forms for display
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }

    # Render the page with the context containing the forms
    return render(request, 'ltreview/create_review_and_ticket.html', context=context)

@login_required  # Ensure only authenticated users can access this view
def edit_ticket(request, ticket_id):
    # Fetch the ticket by ID or return a 404 error if not found
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if the current user is the owner of the ticket
    if request.user != ticket.user:
        # If not, redirect to a page showing the user's posts
        return redirect('user_posts')

    # Handle form submission
    if request.method == 'POST':
        # Populate the form with data from the request, specifying the instance to update
        form = TicketForm(request.POST, instance=ticket)
        # Validate the form data
        if form.is_valid():
            # Save the updated ticket information to the database
            form.save()
            # Redirect to a page showing the user's posts after successful update
            return redirect('user_posts')
    else:
        # If not a POST request, initialize the form with the existing ticket data
        form = TicketForm(instance=ticket)

    # Prepare the context with the form for rendering
    context = {
        'form': form,
    }

    # Render the edit ticket page with the form
    return render(request, 'ltreview/edit_ticket.html', context)

@login_required  # Ensure only authenticated users can access this view
def delete_ticket(request, ticket_id):
    # Fetch the ticket by ID or return a 404 error if not found
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if the current user is the owner of the ticket
    if request.user == ticket.user:
        # Handle form submission (deletion confirmation)
        if request.method == 'POST':
            # Delete the ticket from the database
            ticket.delete()
            # Redirect to a page showing the user's posts after deletion
            return redirect('user_posts')
        # If not a POST request, render the confirmation page for deletion
        return render(request, 'ltreview/ticket_delete.html')
    else:
        # If the user is not the owner, redirect to a page showing the user's posts
        return redirect('user_posts')

@login_required  # Ensure only authenticated users can access this function
def edit_review(request, review_id):
    # Retrieve the review by its ID, or return a 404 error if it doesn't exist
    review = get_object_or_404(Review, id=review_id)
    
    # Check if the current user is the author of the review
    if request.user != review.author:
        # If not, redirect the user to their posts page as they are not authorized to edit this review
        return redirect('user_posts')

    # Check if the request method is POST, indicating form submission
    if request.method == 'POST':
        # Populate the form with POST data, specifying the review instance to update
        form = ReviewForm(request.POST, instance=review)
        # Validate the form
        if form.is_valid():
            # Save the updated review to the database
            form.save()
            # Redirect the user to their posts page after the review is successfully updated
            return redirect('user_posts')
    else:
        # If the request method is not POST, initialize the form with the review instance for editing
        form = ReviewForm(instance=review)

    # Prepare the form in the context for rendering in the template
    context = {
        'form': form,
    }

    # Render the edit review page with the context containing the form
    return render(request, 'ltreview/edit_review.html', context)

@login_required  # Ensures that only authenticated users can access this function
def delete_review(request, review_id):
    # Attempt to retrieve the specified review by its ID, or return a 404 error if not found
    review = get_object_or_404(Review, id=review_id)
    
    # Verify that the current user is the author of the review
    if request.user == review.author:
        # Check if the deletion has been confirmed through a POST request
        if request.method == 'POST':
            # Delete the review from the database
            review.delete()
            # Redirect the user to their posts page after successful deletion
            return redirect('user_posts')
        # If the request is not POST (e.g., GET), render the confirmation page for deletion
        return render(request, 'ltreview/review_delete.html')
    else:
        # If the user is not the author of the review, redirect them to their posts page
        return redirect('user_posts')

@login_required  # Ensure only authenticated users can access this view
def user_posts(request):
    # Get the current logged-in user
    user = request.user
    
    # Fetch all tickets created by the user
    user_tickets = Ticket.objects.filter(user=user)
    
    # Fetch all reviews authored by the user
    user_reviews = Review.objects.filter(author=user)

    # Initialize a list to hold IDs of tickets for which the user has created a review
    tickets_with_review = []

    # Loop through each ticket to check if the user has created a review for it
    for ticket in user_tickets:
        if Review.objects.filter(ticket=ticket, author=user).exists():
            # If a review by the user for this ticket exists, add the ticket's ID to the list
            tickets_with_review.append(ticket.id)

    # Combine and sort tickets and reviews by their creation time, most recent first
    reviews_and_tickets = sorted(
        chain(user_reviews, user_tickets),
        key=lambda instance: instance.time_created, reverse=True
    )

    # Prepare the context with the combined list and the list of ticket IDs for which the user has created reviews
    context = {
        'reviews_and_tickets': reviews_and_tickets,
        'tickets_with_review': tickets_with_review,
    }

    # Render the user posts page with the context
    return render(request, 'ltreview/user_posts.html', context=context)

@login_required  # Ensure only authenticated users can access this view
def follow_users(request):
    # Initialize an empty list for search results
    search_results = []

    # Check if the request method is POST, indicating either a search operation or a follow operation
    if request.method == 'POST':
        # Attempt to get the username from the POST data for searching
        search_user = request.POST.get('search_user', '').strip()
        
        # If a username is provided, perform a search
        if search_user:
            # Search for users whose username contains the search query, excluding the current user
            search_results = User.objects.filter(username__icontains=search_user).exclude(id=request.user.id)
        else:
            # If no search query, attempt to get the user ID for the follow operation
            user_id = request.POST.get('user_id')
            if user_id:
                # Retrieve the user to follow by ID or return a 404 if not found
                user_to_follow = get_object_or_404(User, id=user_id)
                # Add the retrieved user to the current user's list of followed users
                request.user.follows.add(user_to_follow)

    # Render the follow users form page, passing the search results (if any) to the template
    return render(request, 'ltreview/follow_users_form.html', {'search_results': search_results})

@login_required  # Ensure only authenticated users can access this view
def unfollow_user(request, user_id):
    # Attempt to retrieve the user to unfollow by ID or return a 404 error if not found
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Check if the current user is following the user to unfollow
    if request.user in user_to_unfollow.followed_by.all():
        # Remove the user to unfollow from the current user's follows list
        request.user.follows.remove(user_to_unfollow)
    
    # After unfollowing, redirect the user back to the follow users page
    return redirect('follow_users')

@login_required  # Ensure only authenticated users can access this view
def search_users(request):
    # Initialize an empty form for GET requests or non-POST requests
    if request.method == 'POST':
        # Instantiate the search form with data from the request
        search_form = SearchUsersForm(request.POST)
        
        # Validate the form
        if search_form.is_valid():
            # Extract the search query from the validated form data
            query = search_form.cleaned_data['search_user']
            
            # Perform a case-insensitive search for users by username based on the query
            users = User.objects.filter(username__icontains=query)
            
            # Prepare a list of users to return, containing usernames
            users_list = [{'username': user.username} for user in users]
            
            # Return a JsonResponse with the list of users, suitable for AJAX requests
            return JsonResponse({'users': users_list})
    else:
        # For non-POST requests, initialize an empty form
        search_form = SearchUsersForm()

    # Render the search form page, passing the form to the template
    return render(request, 'ltreview/follow_users_form.html', {'search_form': search_form})

