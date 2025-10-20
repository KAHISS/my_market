from .test_catalog_base import CatalogBaseTestCase
from django.urls import reverse, resolve
from catalog import views


class CatalogProfileViewTest(CatalogBaseTestCase):
    def test_profile_page_view_is_correct(self):
        view = resolve(reverse('catalog:profile'))
        self.assertEqual(view.func, views.profile)

    def test_profile_view_returns_200(self):
        response = self.client.get(reverse('catalog:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_loads_correct_template(self):
        response = self.client.get(reverse('catalog:profile'))
        self.assertTemplateUsed(response, 'catalog/pages/client_profile.html')
