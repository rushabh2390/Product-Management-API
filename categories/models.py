from django.db import models
from commons.models import Common, SoftDeleteManager


class Category(Common):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories',
                               on_delete=models.CASCADE)  # Parent-child relationship

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    # def __str__(self):
    #     return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "categories"
