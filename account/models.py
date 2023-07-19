from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=255)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=False, unique=True)
    first_name = models.CharField('first_name', max_length=150)
    last_name = models.CharField('last_name', max_length=100)
    avatar = models.ImageField(upload_to='media', blank=True, default='avatars/default_avatar.png')
    private_account = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
    panding_request = models.ManyToManyField('self', blank=True, related_name='pandingRequest', symmetrical=False)
    blocked_user = models.ManyToManyField('self', blank=True, related_name='user_blocked', symmetrical=False)
    created_date = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField('post.Post', related_name='authors', blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_("Designates whether this user should be treated as active."
                    "Unselect this instead of deleting accounts"))

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    def create_activation_code(self):
        code = str(uuid4())
        self.activation_code = code

    @property
    def is_anonymous(self):
        return False


