from django.urls import reverse, resolve
from catalog import views
from .test_catalog_base import CatalogBaseTestCase
from unittest.mock import patch


class CatalogPaginationViewTest(CatalogBaseTestCase):
    def test_template_show_per_page_correctly(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.context['products'].paginator.per_page, 12)

    @patch('catalog.views.PER_PAGE', new=10)
    def test_catalog_home_is_paginated(self):
        for i in range(22):
            kwargs = {
                'name': f'Product {i}',
                'in_catalog': True,
                'slug': f'product-{i}',
                'barcode': f'barcode-{i}'
            }
            self.make_product(**kwargs)
        response = self.client.get(reverse('catalog:home'))
        products = response.context['products']
        self.assertEqual(products.paginator.num_pages, 3)
        self.assertEqual(len(products.paginator.get_page(1)), 10)
        self.assertEqual(len(products.paginator.get_page(2)), 10)
        self.assertEqual(len(products.paginator.get_page(3)), 2)

    def test_invalid_page_query(self):
        for i in range(8):
            kwargs = {
                'name': f'Product {i}',
                'in_catalog': True,
                'slug': f'product-{i}',
                'barcode': f'barcode-{i}'
            }
            self.make_product(**kwargs)

        with patch('catalog.views.PER_PAGE', new=3):
            response = self.client.get(reverse('catalog:home') + '?page=1A')
            self.assertEqual(response.context['products'].number, 1)

            response = self.client.get(reverse('catalog:home') + '?page=2')
            self.assertEqual(response.context['products'].number, 2)

            response = self.client.get(reverse('catalog:home') + '?page=3')
            self.assertEqual(response.context['products'].number, 3)
