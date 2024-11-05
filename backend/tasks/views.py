"""tasks views module"""

# third
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

# local
from .models import Task
from .serializers import TaskReadSerializer, TaskWriteSerializer


class TaskListView(APIView):
    """
    View class to list all task regardless of they donde attribute
    or to create a new one.
    """
    def get(self, request, format=None):
        """Method to list all tasks."""
        tasks = Task.objects.all()
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """Method to create a new task."""
        serializer = TaskWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """
    View class to retrieve, update and delete a task.
    """
    def get_object(self, pk):
        """Helper function to retrieve an object from the database."""
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk, format=None):
        """Method to get a serialized task."""
        task = self.get_object(pk)
        serializer = TaskReadSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """Method to updated a serialized task instance."""
        task = self.get_object(pk)
        serializer = TaskWriteSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """Method to delete a serialized task."""
        task = self.get_object(pk)        
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskListPendingView(APIView):
    """
    View class to display tasks that aren't marked as done yet.
    """
    def get(self, request, format=None):
        """Method to display pending tasks only."""
        tasks = Task.objects.filter(done=False)
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
