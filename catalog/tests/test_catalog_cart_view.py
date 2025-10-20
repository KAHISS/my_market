from .test_catalog_base import CatalogBaseTestCase
from django.urls import reverse, resolve
from catalog import views


class CatalogCartViewTest(CatalogBaseTestCase):
    def test_cart_page_view_is_correct(self):
        view = resolve(reverse('catalog:cart'))
        self.assertEqual(view.func, views.cart)

    def test_cart_view_returns_200(self):
        response = self.client.get(reverse('catalog:cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart_view_loads_correct_template(self):
        response = self.client.get(reverse('catalog:cart'))
        self.assertTemplateUsed(response, 'catalog/pages/cart.html')
