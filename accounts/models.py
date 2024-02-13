from django.db import models
from django.contrib.auth.models import AbstractUser  # Import Django's built-in AbstractUser class

# Custom User model extending Django's AbstractUser
class User(AbstractUser):
    """
    User model that extends the default Django user model with a follows relationship.
    This model uses a ManyToManyField to represent a non-symmetrical following relationship,
    where users can follow other users without mutual following.
    """
    # Define a ManyToManyField to represent the following relationship between users.
    # 'self' indicates that this relationship is with the same model, i.e., users can follow other users.
    # symmetrical=False makes this relationship non-reciprocal by default (if A follows B, B doesn't necessarily follow A).
    # verbose_name='suit' provides a human-readable name for the relationship.
    # related_name='followed_by' specifies the name to use for the reverse relation from a User instance back to other users following it.
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='suit',
        related_name='followed_by'
    )

    def __str__(self):
        """
        String representation of the User model, returning the user's username.
        """
        return f'{self.username}'

# Commented out UserFollows model, an alternative implementation for user following.
# class UserFollows(models.Model):
#     """
#     An alternative implementation for a user following system, using a separate model to represent follows.
#     Each instance of this model represents a single follow relationship between two users.
#     """
#     # A foreign key linking back to the AUTH_USER_MODEL setting, representing the user who is following.
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # Another foreign key to the same user model, representing the user being followed.
#     # 'related_name' allows accessing all followers of a user.
#     follows_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    
#     class Meta:
#         # Ensures that a user cannot follow another user more than once by setting a unique constraint.
#         unique_together = ('user', 'follows_user')

#     def __str__(self):
#         """
#         String representation of the UserFollows model, returning the followed user's identifier.
#         """
#         return f'{self.follows_user}'
