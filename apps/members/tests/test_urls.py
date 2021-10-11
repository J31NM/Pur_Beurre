from django.test import TestCase
from django.urls import reverse, resolve
from apps.members import views


class TestUrls(TestCase):

    def test_register_url_resolve(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, views.UserRegisterView)

    def test_login_url_resolve(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, views.UserLoginView)

    def test_logout_url_resolve(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, views.UserLogoutView)

    def test_user_account_url_resolve(self):
        url = reverse('user_account')
        self.assertEquals(resolve(url).func.view_class, views.UserAccountView)
