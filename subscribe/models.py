# from django.db import models
# from account.models import CustomUser
#
#
# class Profile(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
#     private_account = models.BooleanField(default=False)
#     followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
#     following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
#     panding_request = models.ManyToManyField('self', blank=True, related_name='pandingRequest', symmetrical=False)
#     blocked_user = models.ManyToManyField('self', blank=True, related_name='user_blocked', symmetrical=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.username}'
#
