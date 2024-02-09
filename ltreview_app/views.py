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


@login_required
def feed(request):
    user = request.user
    # Retrieve tickets created by the logged in user
    user_tickets = Ticket.objects.filter(user=user)

    # Retrieve reviews created by the logged in user
    user_reviews = Review.objects.filter(author=user)

    # retrieve reviews associated with logged in user's tickets
    ticket_reviews = list(chain(*[ticket.review_set.all().exclude(author=user) for ticket in user_tickets]))

    # Retrieve tickets and reviews associated with tracked users
    tickets = Ticket.objects.filter(user__in=user.follows.all())

    # Retrieve reviews associated with followed users
    reviews = Review.objects.filter(
        Q(contributors__in=request.user.follows.all()) | Q(ticket__in=tickets)).exclude(author=user)

    # Create a list to store the IDs of tickets for which the user created a review
    user_has_created_review = []

    # Browse tickets to check if the user created a review
    for ticket in tickets:
        if Review.objects.filter(ticket=ticket, author=user).exists():
            # user created a review for this ticket, add ticket ID to the list
            user_has_created_review.append(ticket.id)

    # Combine tickets and reviews from the logged in user, as well as those from followed users,
    reviews_and_tickets = sorted(
        chain(user_tickets, reviews, tickets, user_reviews, ticket_reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    context = {
        'reviews_and_tickets': reviews_and_tickets,
        'user_has_created_review': user_has_created_review,
    }
    return render(request, 'ltreview/feed.html', context=context)


@login_required
def ticket_create(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    return render(request, 'ltreview/ticket_create.html', context={'ticket_form': ticket_form})


@login_required
def create_review_from_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.ticket = ticket
            review.save()
            review.contributors.add(request.user, through_defaults={'contribution': 'Main author'})
            return redirect('feed')

    context = {
        'review_form': review_form,
        'ticket': ticket,
    }
    return render(request, 'ltreview/create_review_from_ticket.html', context=context)


@login_required
def review_and_ticket_create(request):
    review_form = ReviewForm()
    ticket_form = TicketForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.ticket = ticket  # Associe la review au ticket
            review.save()
            review.contributors.add(request.user, through_defaults={'contribution': 'Main author'})
        return redirect('feed')

    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'ltreview/create_review_and_ticket.html', context=context)


# View to edit a ticket
@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('user_posts')

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
    }
    return render(request, 'ltreview/edit_ticket.html', context)


# view to delete ticket
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user == ticket.user:
        if request.method == 'POST':
            ticket.delete()
            return redirect('user_posts')
        return render(request, 'ltreview/ticket_delete.html')
    else:
        return redirect('user_posts')


# view to edit review
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.author:
        return redirect('user_posts')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
    }
    return render(request, 'ltreview/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.author:
        if request.method == 'POST':
            review.delete()
            return redirect('user_posts')
        return render(request, 'ltreview/review_delete.html')
    else:
        return redirect('user_posts')


@login_required
def user_posts(request):
    user = request.user
    user_tickets = Ticket.objects.filter(user=user)
    user_reviews = Review.objects.filter(author=user)

    # Créez une liste pour stocker les IDs des tickets pour lesquels l'utilisateur a créé une review
    tickets_with_review = []

    # Parcourez les tickets pour vérifier si l'utilisateur a créé une review pour chaque ticket
    for ticket in user_tickets:
        if Review.objects.filter(ticket=ticket, author=user).exists():
            # Si l'utilisateur a créé une review pour ce ticket, ajoutez son ID à la liste
            tickets_with_review.append(ticket.id)

    # Créez une liste qui combine les reviews et les tickets de l'utilisateur
    reviews_and_tickets = sorted(
        chain(user_reviews, user_tickets),
        key=lambda instance: instance.time_created, reverse=True
    )

    context = {
        'reviews_and_tickets': reviews_and_tickets,
        'tickets_with_review': tickets_with_review,
    }

    return render(request, 'ltreview/user_posts.html', context=context)


@login_required
def follow_users(request):
    search_results = []

    if request.method == 'POST':
        search_user = request.POST.get('search_user', '').strip()
        if search_user:
            search_results = User.objects.filter(username__icontains=search_user).exclude(id=request.user.id)

        else:
            user_id = request.POST.get('user_id')
            if user_id:
                user_to_follow = get_object_or_404(User, id=user_id)
                request.user.follows.add(user_to_follow)

    return render(request, 'ltreview/follow_users_form.html', {'search_results': search_results})


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    if request.user in user_to_unfollow.followed_by.all():
        request.user.follows.remove(user_to_unfollow)
    return redirect('follow_users')


@login_required
def search_users(request):
    if request.method == 'POST':
        search_form = SearchUsersForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data['search_user']
            users = User.objects.filter(username__icontains=query)
            users_list = [{'username': user.username} for user in users]
            return JsonResponse({'users': users_list})
    else:
        search_form = SearchUsersForm()
    return render(request, 'ltreview/follow_users_form.html', {'search_form': search_form})
