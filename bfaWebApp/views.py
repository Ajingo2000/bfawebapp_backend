from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q, F
from.models import *
from bfaWebBlog.models import *
from bfaSermons.models import *
from django.http import JsonResponse, response 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from.serializers import *
from django.core.mail import send_mail

def home(request):
    return HttpResponse("Welcome to the Django API")
# Create your views here.
@api_view(['GET'])
def index(request):
    blogposts = Post.objects.all()
    recentposts = Post.objects.all().order_by('-created')[:3]
    popularposts = Post.objects.all().order_by('-views')[:1]
    trendingposts = Post.objects.all().order_by('-views')[:3]
    editors_pick = Post.objects.filter(editors_pick=True)
    categories = Category.objects.all()
    authors = Author.objects.all()

    serializer = PostSerializer(blogposts, many=True)
    
    context = {
        'blogposts': blogposts,
        'previous_page': request.META.get('HTTP_REFERER'),
        'recentposts': recentposts,
        'trendingposts': trendingposts,
        'popularposts': popularposts,
        'categories': categories,
        'authors': authors,
        'editors_pick': editors_pick,
    }
   
    return Response(serializer.data)

class BlogPostListView(ListAPIView):
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name', 'category__title', 'tags__tag']

class BlogPostSearchView(ListAPIView):
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Override the get_queryset method to access the query parameter 'query'
        and filter the results accordingly.
        """
        query = self.request.GET.get('query')  # Access the query parameter
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(author__slug__icontains=query))
        else:
            return Post.objects.none()  # Return an empty queryset if no query is provided


class BlogPost_PopularListView(ListAPIView):
    queryset = Post.objects.all().order_by('-views')
    serializer_class = PostSerializer
    lookup_field = 'slug'

class BlogPost_TrendingListView(ListAPIView):
    queryset = Post.objects.all().order_by('-views')
    serializer_class = PostSerializer
    lookup_field = 'slug'

class BlogPost_EditorsPickListView(ListAPIView):
    queryset = Post.objects.all().filter(editors_pick=True)
    serializer_class = PostSerializer
    lookup_field = 'slug'

class BlogPostDetailsView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_object(self):
        obj = super().get_object()
        ip = self.request.META.get('REMOTE_ADDR')
        ip_instance, created = IpModel.objects.get_or_create(ip=ip)
        
        if not obj.views.filter(ip=ip).exists():
            obj.views.add(ip_instance)
            obj.save()

        return obj
    

class TagsListView(ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'tag'


class AuthorListView(ListAPIView):
    queryset = Author.objects.all().order_by('-name')
    serializer_class = AuthorSerializer
    lookup_field = 'name'

class AuthorDetailsView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'name'

class CategoryListView(ListAPIView):
    queryset = Category.objects.all().order_by('-title')
    serializer_class = CategorySerializer
    lookup_field = 'title'

class CategoryDetailsView(RetrieveAPIView):
    queryset = Category.objects.all().order_by('-title')
    serializer_class = CategorySerializer
    lookup_field = 'title'


class BibleBookListView(ListAPIView):
    queryset = BibleBook.objects.all().order_by('-name')
    serializer_class = SermonBibleBookSerializer
    lookup_field = 'slug'

class BibleBookDetailsView(RetrieveAPIView):
    queryset = BibleBook.objects.all().order_by('-name')
    serializer_class = SermonBibleBookSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.lookup_field)
        try:
            bible_book = BibleBook.objects.get(slug=slug)
            sermons = Sermon.objects.filter(bibleBook=bible_book, isExpository=True)
            serializer = self.get_serializer(bible_book)
            data = serializer.data
            data['sermons'] = SermonSerializer(sermons, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except BibleBook.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

# COMMENTS AND REPLIES CREATION VIEWS 
from rest_framework import generics
# COMMENTS 
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# REPLIES 
class ReplyCreateView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class SermonListView(ListAPIView):
    queryset = Sermon.objects.all().order_by('-upload_date')
    serializer_class = SermonSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']

class SermonDetailsView(RetrieveAPIView):
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']


# BIOGRAPHICAL SERMONS
class BiographicalSermonsView(ListAPIView):
    queryset = Sermon.objects.all().filter(sermon_category__title="Biographical")
    serializer_class = SermonSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']

# DOCTRINAL SERMONS
class DoctrinalSermonsView(ListAPIView):
    queryset = Sermon.objects.all().filter(sermon_category__title="Doctrinal")
    serializer_class = SermonSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']

# PRACTICAL SERMONS
class PracticalSermonsView(ListAPIView):
    queryset = Sermon.objects.all().filter(sermon_category__title="Practical")
    serializer_class = SermonSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']

# EXPOSITORY SERMONS
class ExpositorySermonsView(ListAPIView):
    queryset = Sermon.objects.all().filter(sermon_category__title="Expository")
    serializer_class = SermonSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']


class ExpositoryDetailsView(RetrieveAPIView):
    queryset = Sermon.objects.all().filter(sermon_category__title='Expository')
    serializer_class = SermonSerializer
    lookup_field = 'bible_books'

# SPECIAL VIDEOS 
class SpecialVideosView(ListAPIView):
    queryset = Sermon.objects.all().filter(sermon_category__title="Special")
    serializer_class = SermonSerializer
    lookup_field = 'title'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'preached_by', 'preaching_date']


# SERMONS PLAYLISTS 
# RECENT SERMONS 
class RecentSermonsView(ListAPIView):
    queryset = Sermon.objects.all().order_by("-upload_date")
    serializer_class = SermonSerializer
    lookup_field = 'title'

class SermonByYearPlaylist(ListAPIView):
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    lookup_field = 'title'

#MINISTRY RESOURCES
class NewBelieverDocumentsListView(ListAPIView):
    queryset = NewBelieverDocuments.objects.all().order_by('doc_number')
    serializer_class = NewBelieverDocumentsSerializer  
    lookup_field = 'slug'

class NewBelieverDocumentsDetailsView(RetrieveAPIView):
    queryset = NewBelieverDocuments.objects.all().order_by('-doc_number')
    serializer_class = NewBelieverDocumentsSerializer  
    lookup_field = 'slug'

class SoulWinningLessonsListView(ListAPIView):
    queryset = SoulWinningLessons.objects.all().order_by('-doc_number')
    serializer_class = SoulWinningLessonsSerializer
    lookup_field = 'slug'

class SoulWinningLessonsDetails(RetrieveAPIView):
    queryset = SoulWinningLessons.objects.all().order_by('-doc_number')
    serializer_class =   SoulWinningLessonsSerializer
    lookup_field = 'slug'

class  DiscipleshipLessonsListView(ListAPIView):
    queryset = DiscipleshipLessons.objects.all().order_by('-doc_number')
    serializer_class = DiscipleshipLessonsSerializer 
    lookup_field = 'slug'

class DiscipleshipLessonsDetails(RetrieveAPIView):
    queryset = DiscipleshipLessons.objects.all().order_by('-doc_number')
    serializer_class = DiscipleshipLessonsListView   
    lookup_field = 'slug'

class  DisciplerClassLessonsListView(ListAPIView):
    queryset = DisciplerClassLessons.objects.all().order_by('-doc_number')
    serializer_class = DisciplerClassLessonsSerializer 
    lookup_field = 'slug'


class DisciplerClassLessonsDetails(RetrieveAPIView):
    queryset = DisciplerClassLessons.objects.all().order_by('-doc_number')
    serializer_class = DisciplerClassLessonsSerializer   
    lookup_field = 'slug'


class  BiblicalTheologyLessonsListView(ListAPIView):
    queryset = BiblicalTheologyLessons.objects.all().order_by('-doc_number')
    serializer_class = BiblicalTheologyLessonsSerializer 
    lookup_field = 'slug'


class BiblicalTheologyLessonsDetails(RetrieveAPIView):
    queryset = BiblicalTheologyLessons.objects.all().order_by('-doc_number')
    serializer_class =  BiblicalTheologyLessons
    lookup_field = 'slug'


class  MissionaryLetterListView(ListAPIView):
    queryset = MissionaryLetter.objects.all().order_by('-date_created')
    serializer_class = MissionaryLetterSerializer
    lookup_field = 'slug'



class MissionaryLetterDetails(RetrieveAPIView):
    queryset = MissionaryLetter.objects.all().order_by('-date_created')
    serializer_class = MissionaryLetterSerializer  
    lookup_field = 'slug'


# CONTACT FORM IS HERE FOR EDITING 
class ContactFormView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            full_message = f"Message from {name} ({email}):\n\n{message}"
            
            
            send_mail(subject, full_message, email, ['ajingo1738@gmail.com']) 
            # IN PRODUCTION, CHANGE THIS TO BFA EMAIL

            return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# SUBSCRIBING TO THE NEWSLETTER 
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bfaNewsletter.forms import SubscriptionForm

# @api_view(['POST'])
# def subscribe(request):
#     serializer = NewsletterSubscriptionSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         data = {
#             "email_address": email,
#             "status": "subscribed"
#         }
#         url = f'https://{settings.MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members'
#         response = requests.post(
#             url,
#             auth=('apikey', settings.MAILCHIMP_API_KEY),
#             json=data
#         )
#         if response.status_code in (200, 201):
#             return Response(response.json(), status=status.HTTP_200_OK)
#         else:
#             return Response(response.json(), status=response.status_code)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def subscribe(request):
#     email = request.data.get('email')
#     if not email:
#         return Response({'error': 'Email is required'}, status=400)

#     api_key = 'your_mailerlite_api_key'
#     group_id = 'your_group_id'  # Replace with your actual group_id
#     url = f'https://api.mailerlite.com/api/v2/groups/{group_id}/subscribers'
#     headers = {
#         'Content-Type': 'application/json',
#         'X-MailerLite-ApiKey': api_key
#     }
#     data = {
#         'email': email
#     }
#     response = requests.post(url, json=data, headers=headers)

#     if response.status_code == 200:
#         return Response({'message': 'Subscribed successfully'})
#     else:
#         return Response({'error': 'Failed to subscribe'}, status=500)
    
# SENDPULSE EMAIL SUBSCRIPTION 
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
import logging

from rest_framework.decorators import api_view

load_dotenv()

SENDPULSE_API_URL = "https://api.sendpulse.com"
SENDPULSE_USER_ID = os.getenv('sendpulse_Api_Id')
SENDPULSE_SECRET = os.getenv('sendpulse_Api_Secret')
ADDRESS_BOOK_ID = os.getenv('sendpulse_address_book_id')

# Setup logging
logger = logging.getLogger(__name__)

def get_sendpulse_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': SENDPULSE_USER_ID,
        'client_secret': SENDPULSE_SECRET,
    }
    response = requests.post(f"{SENDPULSE_API_URL}/oauth/access_token", data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        logger.error(f"Failed to get token: {response.text}")
        return None

@csrf_exempt
@api_view(['POST'])
def subscribe(request):
    if request.method == 'POST':
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            token = get_sendpulse_token()
            if not token:
                return JsonResponse({'message': 'Failed to get token'}, status=500)

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            payload = {
                'emails': [email],
            }
            endpoint = f"{SENDPULSE_API_URL}/addressbooks/{ADDRESS_BOOK_ID}/emails"
            logger.info(f"Sending request to {endpoint} with payload: {payload}")

            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                return JsonResponse({'message': 'Subscription successful'}, status=200)
            else:
                logger.error(f"SendPulse API error: {response.text}")
                return JsonResponse({'message': 'Subscription failed'}, status=response.status_code)
        else:
            return JsonResponse({'message': 'Invalid email'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)






