from django.db import models
from django.utils import timezone
# Create your models here.


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        """
        Getting queryset function for Soft Delete models.
        """
        return super().get_queryset().filter(deleted_at__isnull=True)


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
