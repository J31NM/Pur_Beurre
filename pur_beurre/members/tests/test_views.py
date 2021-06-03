from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_account_url = reverse('user_account')

    def test_user_register_view_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_user_login_view_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_logout_view_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)

    def test_user_account_view_GET(self):
        response = self.client.get(self.user_account_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/user_account.html')


    def test_user_register_POST_new_profile(self):
        expected_email = 'test_user@mail.com'
        expected_username = 'test_user'
        data = dict(
            username=expected_username, email=expected_email,
            password1='password0123_test', password2='password0123_test'
        )
        response = self.client.post(self.register_url, data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/members/login/')
        registered_users = User.objects.filter(username=expected_username, email=expected_email)
        self.assertEqual(len(registered_users), 1)

    def test_user_login_view_POST(self):
        data = dict(username='rata', password='touille')
        response = self.client.post(self.login_url, data=data)
        self.assertEquals(response.status_code, 200)
        print(response)

