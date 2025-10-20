from django.urls import reverse, resolve
from .test_catalog_base import CatalogBaseTestCase
from catalog import views


class CatalogProductViewTest(CatalogBaseTestCase):
    def test_product_page_view_is_correct(self):
        self.make_product()
        view = resolve(reverse('catalog:product', kwargs={'product_id': 1}))
        self.assertEqual(view.func, views.product)

    def test_product_view_returns_200(self):
        self.make_product()
        response = self.client.get(
            reverse('catalog:product', kwargs={'product_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_product_view_returns_404_if_product_not_found(self):
        response = self.client.get(
            reverse('catalog:product', kwargs={'product_id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_product_view_template_shows_if_product_exists(self):
        self.make_product()
        response = self.client.get(
            reverse('catalog:product', kwargs={'product_id': 1}))
        self.assertIn('Produto 1', response.content.decode('utf-8'))

    def test_product_view_loads_correct_template(self):
        self.make_product()
        response = self.client.get(
            reverse('catalog:product', kwargs={'product_id': 1}))
        self.assertTemplateUsed(response, 'catalog/pages/product.html')

    def test_product_view_dont_load_products_not_published(self):
        self.make_product(in_catalog=False)
        response = self.client.get(
            reverse('catalog:product', kwargs={'product_id': 1}))
        self.assertEqual(response.status_code, 404)
