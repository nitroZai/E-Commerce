
from django.urls import reverse
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(
        upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
