
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from django_quill.fields import QuillField
import uuid
from .utils import get_read_time
import datetime
import re
import math
from django.utils.html import strip_tags
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify


# Create your models here.
class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Tags(models.Model):
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag

class Post(models.Model):
    title = models.CharField(max_length=500)
    image= models.ImageField(upload_to='img')
    body = HTMLField()
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='posts')
    # likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name="posts")
    # read_time = models.DateTimeField( blank=True, null=True)
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    editors_pick = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True, null=True, related_name="posts", )

    

    def calculate_read_time(self):
        word_count = len(strip_tags(self.body).split())  # Simplified word count
        read_time = str(datetime.timedelta(minutes=math.ceil(word_count / 200)))        
        return read_time

    def __str__(self):
        original_slug = slugify(self.title)
        queryset = Post.objects.all().filter(slug__iexact=original_slug).count()
        return self.title


    def total_views(self):
        return self.views.count()    
    
    def save(self, *args, **kwargs):
            # Call the original save method
            super().save(*args, **kwargs)

            # Incase a slug with the same name solution
            original_slug = slugify(self.title)
            queryset = Post.objects.all().filter(slug__iexact=original_slug).count()
            count = 1
            slug = original_slug
            while(queryset):
                slug = original_slug + '-' + str(count)
                count += 1
                queryset = Post.objects.all().filter(slug__iexact=slug).count()
    
    class Meta:
        ordering = ['-created']


class Author(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="profile-images")
    email = models.EmailField()
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200) 

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    comment_id = models.UUIDField(max_length=100 ,default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content[:50]}'
    
    class Meta:
        ordering = ['-created_at']

class Reply(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    id = models.UUIDField(max_length=100 ,default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content[:50]}'
    
    class Meta:
        ordering = ['-created_at']