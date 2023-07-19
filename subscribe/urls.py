from django.urls.conf import path
from .views import FollowUnfollowView

urlpatterns = [
    path('follow_unfollow/', FollowUnfollowView.as_view(), name="follow_unfollow"),
]
