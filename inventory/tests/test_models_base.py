from inventory.models import Product, Category
from django.test import TestCase


class ModelsBaseTestCase(TestCase):
    def setUp(self):
        return super().setUp()

    def make_category(self, name='Categoria 1'):
        return Category.objects.create(name=name)

    def make_product(
            self,
            category_data=None,
            barcode='1234567890123',
            name='Produto 1',
            brand='Marca 1',
            slug="produto-1",
            description='Descrição do produto 1',
            packaging_type='unidade',
            sale_price=100.00,
            purchase_price=80.00,
            discount=0.00,
            minimum_stock=10,
            stock_quantity=20,
            in_catalog=True
    ):
        if category_data is None:
            category_data = {}

        product = Product(
            barcode=barcode,
            name=name,
            brand=brand,
            slug=slug,
            description=description,
            packaging_type=packaging_type,
            category=self.make_category(**category_data),
            sale_price=sale_price,
            purchase_price=purchase_price,
            discount=discount,
            minimum_stock=minimum_stock,
            stock_quantity=stock_quantity,
            in_catalog=in_catalog,
        )
        return product
