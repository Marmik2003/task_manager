from django.test import TestCase

from tasks.models import Task, TaskHistory, UserTaskReportSetting


# Test case for Task model
class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='Test task', description='Test description')
        self.task.status = 'COMPLETED'
        self.task.save()

    def test_task_creation(self):
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)

    def test_task_creation_with_history(self):
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)
        self.assertEqual(self.task.history.count(), 1)

    def test_task_creation_with_history_and_status(self):
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)
        self.assertEqual(self.task.history.count(), 1)
        self.assertEqual(self.task.history.first().status, 'PENDING')

    def test_task_creation_with_history_and_status_and_user(self):
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)
        self.assertEqual(self.task.history.count(), 1)
        self.assertEqual(self.task.history.first().status, 'PENDING')
        self.assertEqual(self.task.history.first().user, self.task.user)
