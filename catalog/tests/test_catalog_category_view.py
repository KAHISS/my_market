from .test_catalog_base import CatalogBaseTestCase
from django.urls import reverse, resolve
from catalog import views


class CatalogCategoryViewTest(CatalogBaseTestCase):
    def test_category_page_view_is_correct(self):
        self.make_category()
        view = resolve(reverse("catalog:category", kwargs={'category_id': 1}))
        self.assertEqual(view.func, views.category)

    def test_category_view_returns_200(self):
        self.make_category()
        response = self.client.get(
            reverse('catalog:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_category_view_loads_correct_template(self):
        self.make_category()
        response = self.client.get(
            reverse('catalog:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'catalog/pages/category.html')

    def test_category_template_shows_no_itens_found_if_no_products(self):
        self.make_category()
        response = self.client.get(
            reverse('catalog:category', kwargs={'category_id': 1}))
        self.assertIn('Nenhum produto encontrado',
                      response.content.decode('utf-8'))

    def test_category_template_shows_products_if_products_exist(self):
        self.make_product()
        response = self.client.get(
            reverse('catalog:category', kwargs={'category_id': 1}))
        self.assertIn('Produto 1', response.content.decode('utf-8'))

    def test_category_template_dont_load_products_not_published(self):
        self.make_product(in_catalog=False)
        response = self.client.get(
            reverse('catalog:category', kwargs={'category_id': 1}))
        self.assertNotIn('Produto 1', response.content.decode('utf-8'))
