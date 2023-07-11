from django.db import models
from account.models import CustomUser
from category.models import Category


class Post(models.Model):
    title = models.CharField(max_length=100)
    post = models.ImageField(upload_to='media/images/', )
    owner = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id', ]


