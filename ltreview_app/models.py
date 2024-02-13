from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Define a Ticket model to represent tickets in the system.
class Ticket(models.Model):
    # Define fields for the Ticket model.
    title = models.CharField(max_length=100, default='Titre par défaut')  # Title of the ticket with a default value.
    description = models.TextField(default='Description par défaut')  # Description of the ticket with a default value.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Link to the user who created the ticket. It's nullable.
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Optional image for the ticket.
    time_created = models.DateTimeField(auto_now_add=True)  # Timestamp of when the ticket was created.

    # String representation of the Ticket model.
    def __str__(self):
        return f'{self.title}'

# Define a Review model to represent reviews related to tickets.
class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)  # Link to the ticket being reviewed.
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating given to the ticket, validated between 1 and 5.
    headline = models.CharField(max_length=128, default='Titre de la critique')  # Headline of the review with a default value.
    body = models.CharField(max_length=8192, blank=True)  # Optional detailed body of the review.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the author of the review.
    time_created = models.DateTimeField(auto_now_add=True)  # Timestamp of when the review was created.
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='ReviewContributor', related_name='contributions')  # Many-to-many relationship to track contributors to the review.

    # String representation of the Review model.
    def __str__(self):
        return f'{self.headline}'
    
# Define a ReviewContributor model to represent contributions to reviews.
class ReviewContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the user contributing to the review.
    review = models.ForeignKey(Review, on_delete=models.CASCADE)  # Link to the review to which the contribution is made.
    contribution = models.CharField(max_length=255, blank=True)  # Description of the contribution, optional.

    # Meta class to ensure uniqueness of contribution per contributor-review pair.
    class meta:
        unique_together = ('contributor', 'review')  # Ensures a user can only be a contributor to a review once.
