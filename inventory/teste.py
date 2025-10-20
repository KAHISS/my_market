from models import Product

product = Product.objects.all()

for index, p in enumerate(product):
    p.slug = f"{p.name}-{p.brand}-{index}".replace(" ", "-").lower()
    p.save()
