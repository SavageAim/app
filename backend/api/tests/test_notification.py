from datetime import timedelta
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from api.models import Notification
from api.serializers import NotificationSerializer
from .test_base import SavageAimTestCase


class NotificationCollection(SavageAimTestCase):
    """
    Get a list of Notifications and make sure the correct list is returned
    """

    def tearDown(self):
        Notification.objects.all().delete()

    def test_list(self):
        """
        Create some Notification objects in the DB, send an api request and ensure that they all are returned correctly
        """
        mid_notif = Notification.objects.create(
            link='/link/',
            text='This is a Test Notification',
            type='status_message',
            user=self._get_user(),
        )
        mid_notif.timestamp = timezone.now() - timedelta(hours=2)
        mid_notif.save()
        Notification.objects.create(
            link='/link/new/',
            text='This is a Test Notification too but it comes later',
            type='status_message',
            user=self._get_user(),
        )
        old_notif = Notification.objects.create(
            link='/link/old/',
            text='This is a Test Notification but is the earliest and therefore is last in the list',
            type='status_message',
            user=self._get_user(),
        )
        old_notif.timestamp = timezone.now() - timedelta(days=1)
        old_notif.save()

        order = ['/link/new/', '/link/', '/link/old/']

        url = reverse('api:notification_collection')
        user = self._get_user()
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for index, item in enumerate(response.json()):
            self.assertEqual(item['link'], order[index])

        # Add filters and test as well
        filter_url = f'{url}?unread=true'
        old_notif.read = True
        old_notif.save()
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(len(content), 2)
        self.assertTrue(old_notif.pk not in map(lambda item: item['id'], content))

        filter_url = f'{url}?limit=2'
        old_notif.read = False
        old_notif.save()
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(len(content), 2)
        self.assertTrue(old_notif.pk not in map(lambda item: item['id'], content))

        filter_url = f'{url}?limit=2&unread=1'
        mid_notif.read = True
        mid_notif.save()
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(len(content), 2)
        self.assertTrue(mid_notif.pk not in map(lambda item: item['id'], content))

    def test_mark_as_read(self):
        """
        Create two notifications, ensure they are unread, then send a request to mark them both as read and ensure they
        are updated accordingly
        """
        url = reverse('api:notification_collection')
        user = self._get_user()
        self.client.force_authenticate(user)

        notif1 = Notification.objects.create(
            link='/link/new/',
            text='This is a Test Notification',
            type='status_message',
            user=user,
        )
        notif2 = Notification.objects.create(
            link='/link/new/',
            text='This is a Test Notification',
            type='status_message',
            user=user,
        )
        self.assertFalse(notif1.read)
        self.assertFalse(notif2.read)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notif1.refresh_from_db()
        notif2.refresh_from_db()
        self.assertTrue(notif1.read)
        self.assertTrue(notif2.read)


class NotificationResource(SavageAimTestCase):
    """
    Testing the individual notification methods
    """

    def tearDown(self):
        Notification.objects.all().delete()

    def test_mark_as_read(self):
        """
        Create two notifications, ensure they are unread, then send a request to mark them both as read and ensure they
        are updated accordingly
        """
        user = self._get_user()
        self.client.force_authenticate(user)

        notif1 = Notification.objects.create(
            link='/link/new/',
            text='This is a Test Notification',
            type='status_message',
            user=user,
        )
        notif2 = Notification.objects.create(
            link='/link/new/',
            text='This is a Test Notification',
            type='status_message',
            user=user,
        )
        self.assertFalse(notif1.read)
        self.assertFalse(notif2.read)

        url = reverse('api:notification_resource', kwargs={'pk': notif2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notif1.refresh_from_db()
        notif2.refresh_from_db()
        self.assertFalse(notif1.read)
        self.assertTrue(notif2.read)
