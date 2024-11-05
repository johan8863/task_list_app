"""tasks models module"""

# django
from django.db import models


class Task(models.Model):
    """Model to register personal tasks."""
    name = models.CharField(max_length=200)
    content = models.TextField()
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=False)

    class Meta:
        """Config object class"""

        # if a task was updated should be moved to the top
        ordering = ['updated', 'created']

    def __str__(self) -> str:
        """String method to identify object representation"""
        return self.name