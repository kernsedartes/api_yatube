from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from posts.models import Post, Group, Comment, User
import datetime as dt


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts', 'comments')
        ref_name = 'ReadOnlyUsers'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', default=serializers.CurrentUserDefault()
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=True
    )
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        
    def validate(self, data):
        request = self.context.get('request')
        if request and not request.user.is_authenticated:
            raise ValidationError(
                {"error": "Authentication required"},
                code=status.HTTP_401_UNAUTHORIZED
            )
        return data 


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        
    # def validate(self, data):
    #     request = self.context.get('request')
    #     if request and not request.user.is_authenticated:
    #         raise ValidationError(
    #             {"error": "Authentication required"},
    #             code=status.HTTP_401_UNAUTHORIZED
    #         )
    #     return data
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')