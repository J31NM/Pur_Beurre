from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from products import views


class TestViews(TestCase):

    def SetUp(self):
        self.client = Client()
        self.index_url = reverse('home')
        self.detail_url = reverse('details')

    def test_index(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')