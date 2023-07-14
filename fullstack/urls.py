from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('post.urls')),
    path('comments/', include('comment.urls')),
    path('categories/', include('category.urls')),
    path('likes/', include('like.urls')),
    path('accounts/', include('account.urls')),
    path('followers/', include('subscribe.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)