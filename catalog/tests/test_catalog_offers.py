from django.urls import reverse, resolve
from catalog import views
from .test_catalog_base import CatalogBaseTestCase


class CatalogOffersViewTest(CatalogBaseTestCase):
    def test_catalog_offers_page_view_is_correct(self):
        view = resolve(reverse("catalog:offer"))
        self.assertEqual(view.func, views.offer)

    def test_catalog_offers_view_returns_200(self):
        response = self.client.get(reverse('catalog:offer'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_offers_view_loads_correct_template(self):
        response = self.client.get(reverse('catalog:offer'))
        self.assertTemplateUsed(response, 'catalog/pages/offer.html')

    def test_catalog_offers_template_shows_no_itens_found_if_no_products(self):
        response = self.client.get(reverse('catalog:offer'))
        self.assertIn('Nenhuma oferta encontrada',
                      response.content.decode('utf-8'))

    def test_catalog_offers_template_shows_products_if_products_exist(self):
        self.make_product(discount=10)
        response = self.client.get(reverse('catalog:offer'))
        content = response.content.decode('utf-8')
        self.assertIn('Produto 1', content)
        self.assertIn('Marca 1', content)

    def test_catalog_offers_template_dont_load_products_not_published(self):
        self.make_product(discount=10, in_catalog=False)
        response = self.client.get(reverse('catalog:offer'))
        self.assertNotIn('Produto 1', response.content.decode('utf-8'))
