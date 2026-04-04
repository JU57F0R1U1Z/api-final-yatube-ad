from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        if 'request' in self.context:
            user = self.context['request'].user
            following = data.get('following')
            if following and Follow.objects.filter(user=user, following=following).exists():
                raise serializers.ValidationError(
                    {'following': ['Вы уже подписаны на этого пользователя']}
                )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        following = validated_data.pop('following')
        return Follow.objects.create(user=user, following=following)

    def validate_following(self, value):
        if 'request' in self.context:
            if value == self.context['request'].user:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя!'
                )
        return value
