from typing import Any
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """
    Represents a company entity.
    Each company can have multiple associated user profiles.
    """

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        String representation of the Company.
        """
        return self.name


class Profile(models.Model):
    """
    Represents a user's profile, linking them to a specific company.
    Each user has exactly one profile.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')

    def __str__(self) -> str:
        """
        String representation of the Profile.
        """
        return self.user.username
