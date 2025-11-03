from utils.browser import make_chrome_driver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from catalog.tests.test_catalog_base import CatalogMixin


class CatalogBaseFunctionalTest(StaticLiveServerTestCase, CatalogMixin):
    def setUp(self):
        self.driver = make_chrome_driver()
        return super().setUp()

    def tearDown(self):
        self.driver.quit()
        return super().tearDown()
