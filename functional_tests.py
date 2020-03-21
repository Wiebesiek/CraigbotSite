from selenium.webdriver import Chrome
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from django.shortcuts import render
import unittest


class NewUserTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = Chrome()
        self.test_user = User.objects.create_user(username='testUser',
                                                  password='Django240',
                                                  email='testUser@django.com')
        self.client = Client()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_navigate_to_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code,200)


if __name__ == '__main__':
    unittest.main()