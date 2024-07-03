from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponse
from social_django.models import UserSocialAuth
from .models import Post, Comment ,Reply, IpModel, Category, Author
from .forms import CommentForm, ReplyForm
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
import requests
from django.db.models import Count, Q

from bfaNewsletter.models import Subscriber, EmailTemplate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q

    
def login(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect('/home/')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        return ip
    

@login_required
def home(request):
   blogposts = Post.objects.all()
   recentposts = Post.objects.all().order_by('-created')[:6]
   popularposts = Post.objects.all().order_by('-views')[:1]
   trendingposts = Post.objects.all().order_by('-views')[:3]
   editors_pick = Post.objects.filter(editors_pick=True)
   categories = Category.objects.all()
   authors = Author.objects.all()
   
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
   return render(request, 'home.html', context)

from django.http import JsonResponse

def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    blogposts = comment.parent_post  
    reply_form = ReplyForm(request.POST)

    if reply_form.is_valid():
        parent_comment_id = request.POST.get('parent_comment_id')
        parent_comment = Comment.objects.get(comment_id=parent_comment_id)
        new_reply = reply_form.save(commit=False)
        new_reply.user = request.user
        new_reply.parent_comment = parent_comment
        new_reply.save()

        # Assuming you have a template for rendering a single reply
        reply_html = render_to_string('reply-partial.html', {'reply': new_reply}, request=request)

        return JsonResponse({'success': True, 'reply_html': reply_html})
    else:
        reply_form = ReplyForm()
        context = {
            "blogposts": blogposts,
            'reply_form': reply_form,
        }

    return render(request, 'blog-details.html', context)


def blogDetails(request, slug):
    blogposts = get_object_or_404(Post, slug=slug)
    post = Post.objects.get(slug=slug)
    comments = post.comments.all()
    categories = Category.objects.all()
    categories_with_post_count = Category.objects.annotate(post_count=Count('posts'))
    authors = Author.objects.all()
    latest_post = Post.objects.all().order_by('-created')[:3]

    ip = get_client_ip(request)
    
    if IpModel.objects.filter(ip=ip).exists():
        print('Already exists')
    else:
        IpModel.objects.create(ip=ip)
        post.views.add(IpModel.objects.get(ip=ip))


    
    context = {
        "title": blogposts.title,
        "blogposts": blogposts,
        "post": post,
        "comments": comments,
        'categories': categories,
        'authors': authors,
        'latest_post': latest_post,
        'previous_page': request.META.get('HTTP_REFERER'),
        'categories_with_post_count': categories_with_post_count,
    }

    return render(request, 'post-details.html', context)




def searchblogs(request):
    query = request.GET['query']
    search_results = Post.objects.filter(title__icontains=query) | Post.objects.filter(author__name__icontains=query)

    context = {
        'search_results':search_results,
        'query': query
    }

    return render(request, 'search-results.html', context)