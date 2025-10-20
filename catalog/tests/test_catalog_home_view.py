from django.urls import reverse, resolve
from catalog import views
from .test_catalog_base import CatalogBaseTestCase


class CatalogHomeViewTest(CatalogBaseTestCase):
    def test_catalog_page_view_is_correct(self):
        view = resolve(reverse("catalog:home"))
        self.assertEqual(view.func, views.catalog)

    def test_catalog_view_returns_200(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_view_loads_correct_template(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertTemplateUsed(response, 'catalog/pages/catalogo.html')

    def test_catalog_template_shows_no_itens_found_if_no_products(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertIn('Nenhum produto encontrado',
                      response.content.decode('utf-8'))

    def test_catalog_template_shows_products_if_products_exist(self):
        self.make_product()
        response = self.client.get(reverse('catalog:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Produto 1', content)
        self.assertIn('Marca 1', content)

    def test_catalog_home_template_dont_load_products_not_published(self):
        self.make_product(in_catalog=False)
        response = self.client.get(reverse('catalog:home'))
        self.assertNotIn('Produto 1', response.content.decode('utf-8'))
