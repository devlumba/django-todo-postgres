from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError

import datetime

from myapp.forms import TaskCreateForm, TaskUpdateForm
from myapp.models import TODOList


class GenericTests(TestCase):
    def test_home200(self):
        client = Client()

        response = client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_create_task_via_view_302(self):
        client = Client()
        form_data = {"title": "test-task", "description": "a test task", "expiration_date": "2025-11-02"}

        response = client.post(reverse("task-create"), data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_create_task_via_form(self):
        form_data = {"title": "test-task", "description": "a test task", "expiration_date": "2025-11-02"}
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        print("Form is valid") if form.is_valid() else "Form isn't valid"

        form.save()
        self.assertEqual(TODOList.objects.first().title, "test-task")
        print("title checked")

        self.assertEqual(TODOList.objects.first().expiration_date, datetime.date(2025, 11, 2))
        print("exp date checked")

    def test_update_task_via_form(self):
        form_data = {"title": "test-task", "description": "a test task", "expiration_date": "2025-11-02"}
        test_task = TODOList.objects.create(title="test-task",
                                            description="a test task", expiration_date="2025-11-02")
        # both "2025-11-02" and datetime.date(2025-11-02) work here
        form_data = {"title": "test-task-updated",
                     "description": "a test task, but updated", "expiration_date": "2025-11-04"}

        form = TaskUpdateForm(data=form_data, instance=test_task)
        self.assertTrue(form.is_valid())
        print("Form is valid") if form.is_valid() else "Form isn't valid"
        form.save()

        self.assertEqual(TODOList.objects.first().description, "a test task, but updated")
        print("desc checked")
        self.assertEqual(TODOList.objects.first().expiration_date, datetime.date(2025, 11, 4))
        print("exp date checked")

    def test_date_earlier_than_needed(self):
        client = Client()
        data_to_use = {"title": "test-task", "description": "a test task", "expiration_date": "2024-11-02"}
        #
        # with self.assertRaises(ValidationError):  # this seems to be the standard way of testing exceptions
        #     response = client.post(reverse("task-create"), data=data_to_use)

        response = client.post(reverse("task-create"), data=data_to_use)
        self.assertEqual(response.status_code, 200)  # -- form RE-renders instead of info going further, success
        self.assertEqual(TODOList.objects.count(), 0)

    def test_date_403_form(self):
        form_data = {"title": "test-task", "description": "a test task", "expiration_date": "2024-11-02"}
        form = TaskCreateForm(form_data)
        self.assertFalse(form.is_valid())

    def test_delete_task_via_view(self):
        test_task = TODOList.objects.create(title="test-task",
                                            description="a test task", expiration_date="2025-11-02")

        client = Client()
        response = client.post(reverse("task-delete", kwargs={"pk": test_task.pk}))  # works with both id/pk

        self.assertEqual(TODOList.objects.count(), 0)


