from django.db import models
from categories.models import Category
from commons.models import Common, SoftDeleteManager
from django.core.validators import MinValueValidator


class Product(Common):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')  # Foreign key to Category
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    stock_quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(blank=True, null=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = "Products"
        db_table = "products"
