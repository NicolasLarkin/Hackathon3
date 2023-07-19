from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from account.models import CustomUser
from post.serializers import PostListSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, required=True, write_only=True)
    password2 = serializers.CharField(max_length=20, min_length=8, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'avatar', 'username')

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password2 != password:
            raise serializers.ValidationError('Passwords didn\'t match!')
        validate_password(password)
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ProfileDetailSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'private_account', 'created_date', 'avatar', 'posts')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['followers_count'] = instance.followers.count()
        repr['following_count'] = instance.following.count()
        return repr

    def get_followers_count(self, instance):
        return instance.followers.count()

    def get_following_count(self, instance):
        return instance.following.count()
