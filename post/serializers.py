from rest_framework import serializers
from category.models import Category
from rating.serializers import MarkSerializer
from comment.serializers import CommentSerializer
from django.db.models import Avg
from post.models import Post


class PostListSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'user_username', 'category_name', 'post')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['comments_count'] = instance.comments.count()
        user = self.context['request'].user
        repr['is_liked'] = user.likes.filter(post=instance).exists() if user.is_authenticated else False
        repr['is_favorite'] = user.favorites.filter(post=instance).exists() if user.is_authenticated else False
        return repr


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ('category', 'title', 'post')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['comments_count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        repr['likes_count'] = instance.likes.count()
        repr['marks'] = MarkSerializer(instance.marks.all(), many=True).data
        repr['marks_count'] = instance.marks.count()
        marks_count = instance.marks.count()
        total_marks = instance.marks.aggregate(total=Avg('mark'))['total']
        repr['rating'] = total_marks
        user = self.context['request'].user
        repr['is_liked'] = user.likes.filter(post=instance).exists() if user.is_authenticated else False
        repr['is_favorite'] = user.favorites.filter(post=instance).exists() if user.is_authenticated else False
        return repr
