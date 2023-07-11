from django.db import models
from post.models import Post
from account.models import CustomUser


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='liked_posts', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'post']


class Favorite(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='favorites', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favorite', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'post']
