from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from account import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from fullstack.tasks import send_confirmation_email_task
from account.models import CustomUser
from django.shortcuts import redirect


User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny, )

    @action(['POST'], detail=False)
    def register(self, request, *ars, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email_task.delay(user.email, user.activation_code)
            except Exception as e:
                print(e, '!!!!!!')
                return Response({'msg': 'Registered, but troubles with email',
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)

    @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
    def activate(self, request, uuid):
        try:
            user = CustomUser.objects.get(activation_code=uuid)
        except CustomUser.DoesNotExists:
            return Response({'msg': 'Invalid link or link does not expired!'}, status=400)

        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect("http://localhost:3000/login/")


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny, )


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny, )


class ProfileDetailView(GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = CustomUser.objects.all()
    serializer_class = serializers.ProfileDetailSerializer

    @action(detail=True, methods=['GET'])
    def profile_details(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
