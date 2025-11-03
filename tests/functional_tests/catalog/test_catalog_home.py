from selenium.webdriver.common.by import By
from base import CatalogBaseFunctionalTest
import pytest
import time


@pytest.mark.functional_test
class TestCatalogHomeFunctionalTest(CatalogBaseFunctionalTest):

    def test_home_page(self):
        self.driver.get(self.live_server_url + '/catalog/')
        body = self.driver.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhum produto encontrado.', body.text)

    def test_category_page(self):
        product = self.make_product(category_data={'name': 'Categoria 1'})
        self.driver.get(self.live_server_url + '/catalog/')
        category1 = self.driver.find_elements(
            By.CSS_SELECTOR, 'option[value="/catalog/category/1/"]')
        self.assertEqual(category1[0].text, 'Categoria 1')
