"""tasks tests module"""

# django
from django.test import TestCase

# local
from .models import Task

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
