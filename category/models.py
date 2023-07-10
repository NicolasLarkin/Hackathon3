from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
