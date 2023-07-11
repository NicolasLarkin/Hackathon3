from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('post.urls')),
    path('comments/', include('comment.urls')),
    path('likes/', include('like.urls')),
    path('accounts', include('account.urls')),
]
