from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    USER_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('owner', 'Owner'),
        ('guide', 'Guide')
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,
                                 default='regular')
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.username
