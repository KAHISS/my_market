from inventory.models import Product
from .test_models_base import ModelsBaseTestCase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class InventoryModelProductTest(ModelsBaseTestCase):
    def setUp(self):
        self.product = self.make_product()
        self.product.save()
        return super().setUp()

    @parameterized.expand([
        ('barcode', 13),
        ('name', 64),
        ('brand', 64),
    ])
    def test_inventory_model_product_fields_max_length(self, field, max_length):
        setattr(self.product, field, "a" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_inventory_model_product_barcode_unique(self):
        product2 = self.make_product(
            barcode=self.product.barcode, slug="produto-2")
        with self.assertRaises(ValidationError):
            product2.full_clean()

    def test_inventory_model_product_slug_unique(self):
        product2 = self.make_product(
            barcode="45354355", slug=self.product.slug)
        with self.assertRaises(ValidationError):
            product2.full_clean()

    def test_inventory_model_product_in_catalog_is_false_by_default(self):
        product = Product(
            barcode='1234567890129',
            name='Produto 1',
            brand='Marca 1',
            slug='produto-2',
            description='Descrição do produto 1',
            packaging_type='unidade',
            sale_price=100.00,
            purchase_price=80.00,
            discount=0.00,
            minimum_stock=10,
            stock_quantity=20,
        )
        product.full_clean()
        product.save()
        self.assertFalse(product.in_catalog)

    def test_inventory_model_product_string_representation(self):
        self.assertEqual(str(self.product), self.product.name)

    def test_inventory_model_product_get_discounted_price(self):
        self.product.discount = 10
        self.assertEqual(self.product.get_discounted_price(), "90,00")

    def test_inventory_model_product_get_total_price(self):
        self.product.discount = 10
        self.assertEqual(self.product.get_total_price(10), "1000,00")
