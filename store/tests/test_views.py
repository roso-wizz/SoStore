from unittest import skip
from importlib import import_module
from django.conf import settings 

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase #,RequestFactory
from django.urls import reverse

from store.models import Category, Product
from store.views import products_all


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        #self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='Clothes', slug='clothes')
        Product.objects.create(category_id=1, title='Hoodies', created_by_id=1,
                               slug='hoodies', price='49.99', image='images/Hoodie1.jpg')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='agentroso.pythonanywhere.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(
            reverse('store:category_list', args=['clothes']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test items response status
        """
        response = self.c.get(
            reverse('store:product_detail', args=['hoodies']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = products_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>SoShaTvStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    """def test_view_function(self):
        
        #Example: Using request factory
        
        request = self.factory.get('Watches')
        response = products_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>SoShaTVStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)"""
