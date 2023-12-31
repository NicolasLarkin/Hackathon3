from rest_framework import serializers
from account.models import CustomUser


class EachUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'profile_pic')
        read_only_fields = ('id', 'username', 'profile_pic')


class FollowerSerializer(serializers.ModelSerializer):
    followers = EachUserSerializer(many=True, read_only=True)
    following = EachUserSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('followers', 'following')
        read_only_fields = ('followers', 'following')


class BlockPendinSerializer(serializers.ModelSerializer):
    panding_request = EachUserSerializer(many=True, read_only=True)
    blocked_user = EachUserSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('panding_request', 'blocked_user')
        read_only_fields = ('panding_request', 'blocked_user')


