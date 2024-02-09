from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit',
        related_name='followed_by'
    )

    def __str__(self):
        return f'{self.username}'


# class UserFollows(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     follows_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')

#     class Meta:
#         unique_together = ('user', 'follows_user')

#     def __str__(self):
#         return f'{self.follows_user}'

