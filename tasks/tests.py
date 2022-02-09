import time
import datetime

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task, UserTaskReportSetting
from tasks.tasks import send_email_reports


User = get_user_model()


# Test case for Task model
class TaskModelTest(TestCase):
    """
    Test case for TaskHistory model
    """

    def setUp(self):
        self.task = Task.objects.create(title='Test task', description='Test description')
        # Update task status
        self.task.status = 'COMPLETED'
        self.task.save()
        self.task.refresh_from_db()

    def test_task_creation(self):
        """
        Test case for Creation of Task model
        """
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)

    def test_task_creation_with_history(self):
        """
        Test case for Task model with history
        """
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)
        self.assertEqual(self.task.history.count(), 1)

    def test_task_creation_with_history_and_status(self):
        """
        Test case for Task model with history and status
        """
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.__str__(), self.task.title)
        self.assertEqual(self.task.history.count(), 1)
        self.assertEqual(self.task.history.first().new_status, 'PENDING')


# Test case for IndexView
class IndexViewTest(TestCase):
    """
    Test case for IndexView
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_index_view_with_no_tasks(self):
        """
        Test case for IndexView with no tasks
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['all_tasks'].count(), 0)
        self.assertEqual(response.context['count_completed'], 0)

    def test_index_view_with_tasks(self):
        """
        Test case for IndexView with tasks
        """
        Task.objects.create(title='Test task', description='Test description', user=self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['all_tasks'].count(), 1)
        self.assertEqual(response.context['count_completed'], 0)

    def test_index_view_with_completed_tasks(self):
        """
        Test case for IndexView with completed tasks
        """
        Task.objects.create(title='Test task', description='Test description', user=self.user, status='COMPLETED')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['all_tasks'].count(), 1)
        self.assertEqual(response.context['count_completed'], 1)


# Test case for PendingTaskView
class PendingTaskViewTest(TestCase):
    """
    Test case for PendingTaskView
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_pending_task_view_with_no_tasks(self):
        """
        Test case for PendingTaskView with no tasks
        """
        response = self.client.get('/pending/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending_tasks'].count(), 0)
        self.assertEqual(response.context['count_all'], 0)

    def test_pending_task_view_with_tasks(self):
        """
        Test case for PendingTaskView with tasks
        """
        Task.objects.create(title='Test task', description='Test description', user=self.user)
        response = self.client.get('/pending/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending_tasks'].count(), 1)
        self.assertEqual(response.context['count_all'], 1)

    def test_pending_task_view_with_completed_tasks(self):
        """
        Test case for PendingTaskView with completed tasks
        """
        Task.objects.create(title='Test task', description='Test description', user=self.user, status='COMPLETED')
        response = self.client.get('/pending/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending_tasks'].count(), 0)
        self.assertEqual(response.context['count_all'], 1)


# Test case for CompletedTaskView
class CompletedTaskViewTest(TestCase):
    """
    Test case for CompletedTaskView
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_completed_task_view_with_no_tasks(self):
        """
        Test case for CompletedTaskView with no tasks
        """
        response = self.client.get('/completed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['completed_tasks'].count(), 0)
        self.assertEqual(response.context['count_all'], 0)

    def test_completed_task_view_with_tasks(self):
        """
        Test case for CompletedTaskView with tasks
        """
        Task.objects.create(title='Test task', description='Test description', user=self.user, status='COMPLETED')
        response = self.client.get('/completed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['completed_tasks'].count(), 1)
        self.assertEqual(response.context['count_all'], 1)

    def test_completed_task_view_with_pending_tasks(self):
        """
        Test case for CompletedTaskView with pending tasks
        """
        Task.objects.create(title='Test task', description='Test description', user=self.user)
        response = self.client.get('/completed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['completed_tasks'].count(), 0)
        self.assertEqual(response.context['count_all'], 1)


# Test case for Task Creation
class TaskCreationTest(TestCase):
    """
    Test case for Task Creation
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_task_creation_less_than_three_char_title(self):
        """
        Test case for Creation of Task model with less than three characters in title
        """
        post_data = {'title': 'Te', 'description': 'Test description', 'priority': 1, 'status': 'PENDING'}
        response = self.client.post('/add/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_creation_negative_priority(self):
        """
        Test case for Creation of Task model with negative priority
        """
        post_data = {'title': 'Test task', 'description': 'Test description', 'priority': -1, 'status': 'PENDING'}
        response = self.client.post('/add/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_creation(self):
        """
        Test case for Creation of Task model
        """
        post_data = {'title': 'Test task', 'description': 'Test description', 'priority': 1, 'status': 'PENDING'}
        response = self.client.post('/add/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test task')


# Test case for Task Edit
class TaskEditTest(TestCase):
    """
    Test case for Task Edit
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(title='Test task', description='Test description', user=self.user)

    def test_task_edit(self):
        """
        Test case for Edit of Task model
        """
        post_data = {'title': 'Test task2', 'description': 'Test description', 'priority': 1, 'status': 'PENDING'}
        response = self.client.post('/edit/{}/'.format(self.task.id), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test task2')


# Test case for Task Delete
class TaskDeleteTest(TestCase):
    """
    Test case for Task Delete
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(title='Test task', description='Test description', user=self.user)

    def test_task_delete(self):
        """
        Test case for Delete of Task model
        """
        response = self.client.get('/delete/{}/'.format(self.task.id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.first().deleted, True)


# Test case for Scheduling reports
class TaskReportTest(TestCase):
    """
    Test case for Scheduling reports
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(title='Test task', description='Test description', user=self.user)

    def test_task_report(self):
        """
        Test case for Scheduling reports
        """
        post_data = {'usr_email': 'user@gmail.com', 'report_time': '10:00'}
        response = self.client.post('/schedule_reports/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserTaskReportSetting.objects.count(), 1)
        self.assertEqual(UserTaskReportSetting.objects.first().user_id, self.user.id)

    def test_get_report_setting(self):
        """
        Test case for Get report setting
        """
        response = self.client.get('/schedule_reports/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['usr_email'], self.user.email)
        self.assertEqual(response.context['report_time'], None)


################
# API TESTS    #
################

def sample_task(user, **params):
    """Create and return a Test task"""
    defaults = {
        'title': 'Test task',
        'description': 'test description',
        'status': 'PENDING',
        'priority': 1,
    }
    defaults.update(params)

    return Task.objects.create(user=user, **defaults)

class TaskViewsetTest(TestCase):
    """
    Test case for Task List API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.task = sample_task(user=self.user)

    def test_task_list_api(self):
        """
        Test case for Task List API
        """
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test task')

    def test_task_detail_api(self):
        """
        Test case for Task Detail API
        """
        response = self.client.get('/api/tasks/{}/'.format(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test task')

    def test_task_create_api(self):
        """
        Test case for Task Create API
        """
        response = self.client.post('/api/tasks/', {
            'title': 'Test task2',
            'description': 'Test description',
            'priority': 1,
            'status': 'PENDING'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, 'Test task2')

    def test_task_update_api(self):
        """
        Test case for Task Update API
        """
        response = self.client.put('/api/tasks/{}/'.format(self.task.id), {
            'title': 'Test task2',
            'description': 'Test description',
            'priority': 1,
            'status': 'PENDING'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test task2')

    def test_task_delete_api(self):
        """
        Test case for Task Delete API
        """
        response = self.client.delete('/api/tasks/{}/'.format(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class TaskHistoryViewSetTest(TestCase):
    """
    Test case for Task History API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.task = sample_task(user=self.user)

    def test_task_history_list_api(self):
        """
        Test case for Task History List API
        """
        response = self.client.get('/api/tasks/{}/history/'.format(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['new_status'], 'PENDING')

    def test_task_history_detail_api(self):
        """
        Test case for Task History Detail API
        """
        response = self.client.get('/api/tasks/{}/history/{}/'.format(self.task.id, self.task.history.first().id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_status'], 'PENDING')


class SendEmailReportTest(TestCase):
    """
    Test case for Send Email Report Task
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.task = sample_task(user=self.user)
        UserTaskReportSetting.objects.create(user=self.user, report_time=timezone.now() + datetime.timedelta(minutes=-1))

    def test_send_email_report(self):
        """
        Test case for Send Email Report 
        """

        response = send_email_reports()
        self.assertEqual(response, 1)
