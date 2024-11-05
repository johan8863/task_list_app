"""tasks tests module"""

# django
from django.test import TestCase
from django.urls import reverse

# third
from rest_framework.test import APITestCase
from rest_framework import status

# local
from .models import Task
from .serializers import TaskReadSerializer, TaskWriteSerializer

class TaskModelTest(TestCase):
    """
    Test class for Task model CRUD operations.
    """
    fixtures = ['tasks.json']

    def setUp(self) -> None:
        self.task = Task(name='Groceries', content='Buy rice.')

    def test_create_task(self):
        """
        When creating a task, first, it must be a Task instance, second the amount
        of tasks must be increased by one.
        """
        count_before = Task.objects.count()
        self.task.save()
        count_after = Task.objects.count()
        self.assertIsInstance(self.task, Task)
        self.assertEqual(count_after, count_before + 1)
    
    def test_read_task(self):
        """
        Retrieving an task by some of its unique attributes must match the source object.
        """
        # inputs
        task = Task.objects.first()
        retrieved_task_pk = task.pk
        retrieved_task = Task.objects.get(pk=retrieved_task_pk)
        # assertions
        self.assertEqual(retrieved_task, task)
    
    def test_update_task(self):
        """
        After of updating any attribute of the task object, 
        it must match with the new value.
        """
        # inputs
        task = Task.objects.first()
        task.name = 'updated_name'
        task.save()
        # assertions
        self.assertEqual(task.name, 'updated_name')
    
    def test_delete_task(self):
        """
        If a task object is deleted, trying to retrieve it must raise an exception.
        """
        # watching exception raising
        with self.assertRaises(Task.DoesNotExist):
            # inputs
            task = Task.objects.last()
            test_task_pk = task.pk
            task.delete()
            # assertions
            deleted_object = Task.objects.get(pk=test_task_pk)
            self.assertIsNone(deleted_object)


class TaskApiTest(APITestCase):
    """
    Test class for Task api views.
    """
    fixtures = ['tasks.json']

    def setUp(self) -> None:
        self.task_list_url = reverse('tasks_list')
        self.task_pending_url = reverse('tasks_list_pending')
        
        self.tasks = Task.objects.all()
        self.tasks_pending = Task.objects.filter(done=False)
    
    def detail_url(self, pk):
        """Helper function as detail urls require a pk argument"""
        return reverse('tasks_detail', args=(pk,))
    
    def test_get_all_tasks(self):
        """
        Retrieveing all tasks through the api must match the tasks class attr.
        """
        # inputs
        response = self.client.get(self.task_list_url)
        retrieved_tasks = response.data
        serialized_tasks = TaskReadSerializer(self.tasks, many=True).data
        # assertions
        self.assertEqual(retrieved_tasks, serialized_tasks)
    
    def test_post_task(self):
        """
        After of creating a task, the amount of task must increase by 1 
        and the response status code must be 201.
        """
        with self.assertRaises(AssertionError):
            # inputs
            data = {
                'name': 'Post task',
                'content': 'Post content',
                'done': True
            }
            serializer = TaskWriteSerializer(data=data)
            count_tasks_before = Task.objects.count()
            response = self.client.post(self.task_list_url, serializer.data)
            count_tasks_after = Task.objects.count()
            # assertions
            if serializer.is_valid():
                self.assertEqual(count_tasks_after, count_tasks_before + 1)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            else:
                self.assertEqual(count_tasks_after, count_tasks_before)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_task(self):
        """
        Retrieving a task must give a 200 status code 
        response and match the source attributes.
        """
        # inputs
        retrieved_task = Task.objects.first()
        response = self.client.get(self.detail_url(retrieved_task.pk))
        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], retrieved_task.name)
    
    def test_put_task(self):
        """
        After of updating a task, a status code 200 response must be given and
        the new task attrs must match the provided ones.
        """
        with self.assertRaises(AssertionError):
            # inputs
            task = Task.objects.first()
            data = {
                'name': 'Updated name',
                'content': 'Updated content',
                'done': True
            }
            serializer = TaskWriteSerializer(task, data=data)
            response = self.client.put(self.detail_url(task.pk), serializer.data)
            if serializer.is_valid():
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(data['name'], task.name)
            else:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_delete(self):
        """
        Deleting a task must return a status code response 204
        and the amount of objects must decrease by 1
        """
        # inputs
        task = Task.objects.last()
        object_before_count = Task.objects.count()
        response = self.client.delete(self.detail_url(task.pk))
        object_after_count = Task.objects.count()
        # assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(object_after_count, object_before_count - 1)
    
    def test_get_pending_tasks(self):
        """
        Retrieveing pending tasks through the api must match the tasks_pending class attr.
        """
        # inputs
        response = self.client.get(self.task_pending_url)
        retrieved_tasks = response.data
        serialized_tasks = TaskReadSerializer(self.tasks_pending, many=True).data
        # assertions
        self.assertEqual(retrieved_tasks, serialized_tasks)
