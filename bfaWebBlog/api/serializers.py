# serializers.py
from rest_framework import serializers
from ..models import Post, Category, Author, Comment, Reply

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class HomeSerializer(serializers.Serializer):
    blogposts = PostSerializer(many=True)
    recentposts = PostSerializer(many=True)
    trendingposts = PostSerializer(many=True)
    popularposts = PostSerializer(many=True)
    categories = CategorySerializer(many=True)
    authors = AuthorSerializer(many=True)
    editors_pick = PostSerializer(many=True)

class BlogDetailsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
