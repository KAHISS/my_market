from django.test import TestCase
from django.urls import reverse


class CatalogURLsTest(TestCase):
    def test_home_page_is_resolved(self):
        url = reverse('catalog:home')
        self.assertEqual(url, '/catalog/')

    def test_category_page_is_resolved(self):
        url = reverse('catalog:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/catalog/category/1')

    def test_product_page_is_resolved(self):
        url = reverse('catalog:product', kwargs={'product_id': 1})
        self.assertEqual(url, '/catalog/product/1')

    def test_profile_page_is_resolved(self):
        url = reverse('catalog:profile')
        self.assertEqual(url, '/catalog/profile')

    def test_cart_page_is_resolved(self):
        url = reverse('catalog:cart')
        self.assertEqual(url, '/catalog/cart')

    def test_search_page_is_resolved(self):
        url = reverse('catalog:search')
        self.assertEqual(url, '/catalog/search/')
