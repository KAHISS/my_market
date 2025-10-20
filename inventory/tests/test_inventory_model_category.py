from .test_models_base import ModelsBaseTestCase
from django.core.exceptions import ValidationError


class InventoryModelCategoryTest(ModelsBaseTestCase):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()

    def test_inventory_model_category_fields_max_length(self):
        self.category.name = "a" * 65
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_inventory_model_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)
