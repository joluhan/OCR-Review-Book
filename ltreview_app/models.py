from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Ticket(models.Model):
    title = models.CharField(max_length=100, default='Titre par défaut')
    description = models.TextField(default='Description par défaut')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    headline = models.CharField(max_length=128, default='Titre de la critique')
    body = models.CharField(max_length=8192, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='ReviewContributor', related_name='contributions')

    def __str__(self):
        return f'{self.headline}'
    
class ReviewContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)

    class meta:
        # Guaranteed the uniqueness of ReviewContributor for each contributor-review
        unique_together = ('contributor', 'review')
