"""tasks serializer module"""

# third
from rest_framework import serializers

# local
from .models import Task


class TaskWriteSerializer(serializers.ModelSerializer):
    """
    Class to serialize/deserialize Task objects in POST, PUT
    and DELETE methods, due to the fact that created and updated methods
    are not editable.
    """
    class Meta:
        model = Task
        fields = ['id', 'name', 'content']


class TaskReadSerializer(serializers.ModelSerializer):
    """
    Class to serialize/deserialize Task objects in GET method,
    all attributes can be retrieved.
    """
    class Meta:
        model = Task
        fields = ['id', 'name', 'content', 'created', 'updated']
