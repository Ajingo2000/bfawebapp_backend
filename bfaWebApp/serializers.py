# serializers.py
from rest_framework import serializers
from bfaWebApp.models import *
from bfaWebBlog.models import *
from bfaSermons.models import *
from bfaNewsletter.models import *


class IpModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model = IpModel
        fields = '__all__'

class CategorySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuthorSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CommentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReplySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class TagSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer2(read_only=True)
    author = AuthorSerializer2(read_only=True)
    comments = CommentSerializer2(many=True, read_only=True)
    views = IpModelSerializer2(many=True, read_only=True)
    tags = TagSerializer2(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' # Add more fields as needed

class IpModelSerializer(serializers.ModelSerializer):
    post_views = PostSerializer2(many=True, read_only=True)
    class Meta:
        model = IpModel
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    posts = PostSerializer2(many=True, read_only=True)
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer2(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    parent_post = PostSerializer2(read_only=True)
    replies = ReplySerializer2(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    parent_comment = CommentSerializer2(read_only=True)
    class Meta:
        model = Reply
        fields = '__all__'
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class SermonCategorySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Sermon_Category
        fields = '__all__'

class SermonBibleBookSerializer2(serializers.ModelSerializer):
    class Meta:
        model = BibleBook
        fields = '__all__'

class SermonSerializer(serializers.ModelSerializer):
    sermon_category= SermonCategorySerializer2(read_only=True)
    bibleBook = SermonBibleBookSerializer2(read_only=True)

    class Meta:
        model = Sermon
        fields = '__all__'

class SermonSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Sermon
        fields = '__all__'


class SermonSerializer3(serializers.ModelSerializer):
    bibleBook = SermonBibleBookSerializer2(read_only=True)
    sermon_category= SermonCategorySerializer2(read_only=True)
    
    class Meta:
        model = Sermon
        fields = '__all__'


class SermonBibleBookSerializer(serializers.ModelSerializer):
    sermons= SermonSerializer3(many=True, read_only=True)
    class Meta:
        model = BibleBook
        fields = '__all__'

class SermonCategorySerializer(serializers.ModelSerializer):
    sermons= SermonSerializer(read_only=True)
    class Meta:
        model = Sermon_Category
        fields = '__all__'

class NewBelieverDocumentsSerializer(serializers.ModelSerializer):
    pdf_doc = serializers.FileField(use_url=True)  # Ensure URL is used

    class Meta:
        model = NewBelieverDocuments
        fields = '__all__'


class SoulWinningLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoulWinningLessons 
        fields = '__all__'


class DiscipleshipLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  DiscipleshipLessons
        fields = '__all__'


class DisciplerClassLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplerClassLessons
        fields = '__all__'


class BiblicalTheologyLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiblicalTheologyLessons
        fields = '__all__'

class MissionaryLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionaryLetter
        fields = '__all__'

# CONTACT FORM SERIALIZER FOR USER CLIENT, SENDING THE MESSAGE AND EMAIL 
# serializers.py

class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100) 
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()

# NEWSLETTER SUBSCRIPTION SERIALIZER! 
class NewsletterSubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email']

