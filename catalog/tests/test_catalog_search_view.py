from .test_catalog_base import CatalogBaseTestCase
from django.urls import reverse, resolve
from catalog import views


class CatalogSearchViewTest(CatalogBaseTestCase):
    def test_search_page_view_is_correct(self):
        view = resolve(reverse('catalog:search'))
        self.assertEqual(view.func, views.search)

    def test_search_loads_correct_template(self):
        response = self.client.get(reverse('catalog:search') + '?q=teste')
        self.assertTemplateUsed(response, 'catalog/pages/search.html')

    def test_search_raises_404_if_no_terms(self):
        response = self.client.get(reverse('catalog:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('catalog:search') + '?q=t<teste>')
        self.assertIn('Busca por &quot;t&lt;teste&gt;&quot;',
                      response.content.decode('utf-8'))

    def test_search_can_find_product_by_name(self):
        product1 = self.make_product(
            name='Café moido', slug='produto-1', barcode='1234567890123')
        product2 = self.make_product(
            name='Café de queijo', slug='produto-2', barcode='1234567890124')

        response1 = self.client.get(
            reverse('catalog:search') + f'?q={product1.name}')
        response2 = self.client.get(
            reverse('catalog:search') + f'?q={product2.name}')
        response3 = self.client.get(
            reverse('catalog:search') + '?q=Café')

        self.assertIn(product1.name, response1.content.decode('utf-8'))
        self.assertNotIn(product2.name, response1.content.decode('utf-8'))

        self.assertIn(product2.name, response2.content.decode('utf-8'))
        self.assertNotIn(product1.name, response2.content.decode('utf-8'))

        self.assertIn(product1.name, response3.content.decode('utf-8'))
        self.assertIn(product2.name, response3.content.decode('utf-8'))
