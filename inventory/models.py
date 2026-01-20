import uuid
from django.db import models


class Category(models.Model):
    """
    Represent a category of products.
    """
    name = models.CharField("Nome da categoria", max_length=64)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        """
        Return the name of the category.
        """
        return self.name


class Product(models.Model):
    """
    Represent a product in the inventory.
    """
    barcode = models.CharField(
        "Código de barras", max_length=13, blank=True, null=True, unique=True)
    name = models.CharField("Nome do produto", max_length=64)
    brand = models.CharField("Marca", max_length=64, blank=True, null=True)
    description = models.TextField("Descrição", blank=True, null=True)
    slug = models.SlugField("Slug", unique=True)
    packaging_type = models.CharField(
        "Tipo de embalagem", max_length=64, blank=True, null=True, default="Caixa")
    unit_measure = models.CharField(
        "Unidade de medida",
        max_length=64,
        blank=True,
        null=True,
        choices=[
            ("UN", "Unidade"),
            ("L", "Litro"),
            ("KG", "Kilograma"),
            ("G", "Grama"),
            ("ML", "Mililitro"),
            ("GR", "Grão"),
        ],
        default="UN"
    )
    unit_per_packaging = models.IntegerField(
        "Unidades por embalagem", default=1)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name="Categoria")
    in_catalog = models.BooleanField("Em catálogo", default=False)
    image = models.ImageField(
        "Imagem", upload_to='inventory/covers/%Y/%m/%d/', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.name


class Stock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='stock', verbose_name="Produto")
    quantity = models.IntegerField("Quantidade", default=0)
    minimum_stock = models.IntegerField("Estoque mínimo", default=0)
    purchase_price = models.DecimalField(
        "Preço de compra", max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        "Preço de venda", max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(
        "Preço de venda em lote", max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(
        "Desconto", max_digits=10, decimal_places=2, blank=True, null=True)
    due_date = models.DateField("Data de vencimento", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.product.name

        # 🏷️ Preço com desconto
    def get_discounted_price(self):
        """
        Retorna o preço de venda com desconto aplicado.
        """
        price = self.sale_price
        if self.discount:
            price -= (self.discount / 100) * price
        return round(price, 2)

    # 📦 Preço por embalagem
    def get_price_packaging(self):
        """
        Retorna o preço do lote considerando o número de unidades por embalagem.
        """
        base_price = self.get_discounted_price()
        return round(base_price * self.product.unit_per_packaging, 2)

    # 💰 Total por quantidade
    def get_total_price(self, quantity, unit_type="unit", discount=None):
        """
        Retorna o preço total do produto com base na quantidade e tipo de unidade.
        """
        total_units = quantity * \
            self.product.unit_per_packaging if unit_type == "packaging" else quantity
        price_per_unit = self.sale_price

        # aplica desconto adicional, se houver
        if discount:
            price_per_unit -= (discount / 100) * price_per_unit
        elif self.discount:
            price_per_unit -= (self.discount / 100) * price_per_unit

        total = total_units * price_per_unit
        return round(total, 2)

    # 🔻 Reduz estoque
    def reduce_stock(self, quantity, unit_type="unit"):
        """
        Reduz a quantidade do estoque.
        """
        total_units = quantity * \
            self.product.unit_per_packaging if unit_type == "packaging" else quantity
        self.quantity = max(0, self.quantity - total_units)
        self.save()


class ProductPrintTag(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    resume_name = models.CharField(max_length=100, blank=True, null=True)
    use_resume_name = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Etiqueta de produto"
        verbose_name_plural = "Etiquetas de produto"
