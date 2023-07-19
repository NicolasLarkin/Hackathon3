from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from account.views import UserViewSet, ProfileDetailView

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('', ProfileDetailView)

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('refresh/', views.RefreshView.as_view()),
    path('', include(router.urls)),

]
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

