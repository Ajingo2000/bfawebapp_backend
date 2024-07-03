# views.py
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from ..models import Post, Comment, Reply, IpModel, Category, Author
from ..forms import CommentForm, ReplyForm
from django.db.models import Count
from django.template.loader import render_to_string

class HomeView(generics.ListAPIView):
    serializer_class = HomeSerializer

    def get_queryset(self):
        blogposts = Post.objects.all()
        recentposts = Post.objects.all().order_by('-created')[:6]
        popularposts = Post.objects.all().order_by('-views')[:1]
        trendingposts = Post.objects.all().order_by('-views')[:3]
        editors_pick = Post.objects.filter(editors_pick=True)
        categories = Category.objects.all()
        authors = Author.objects.all()

        data = {
            'blogposts': [post.serialize() for post in blogposts],
            'recentposts': [post.serialize() for post in recentposts],
            'trendingposts': [post.serialize() for post in trendingposts],
            'popularposts': [post.serialize() for post in popularposts],
            'categories': [category.serialize() for category in categories],
            'authors': [author.serialize() for author in authors],
            'editors_pick': [post.serialize() for post in editors_pick],
        }

        return data

@api_view(['POST'])
def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    blogposts = comment.parent_post  
    reply_form = ReplyForm(request.data)

    if reply_form.is_valid():
        parent_comment_id = request.data.get('parent_comment_id')
        parent_comment = Comment.objects.get(comment_id=parent_comment_id)
        new_reply = reply_form.save(commit=False)
        new_reply.user = request.user
        new_reply.parent_comment = parent_comment
        new_reply.save()

        # Assuming you have a template for rendering a single reply
        reply_html = render_to_string('reply-partial.html', {'reply': new_reply}, request=request)

        return Response({'success': True, 'reply_html': reply_html})
    else:
        reply_form = ReplyForm()
        context = {
            "blogposts": blogposts,
            'reply_form': reply_form,
        }

    return Response(context)

class BlogDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogDetailsSerializer

    def post(self, request, slug):
        blogpost = self.get_object()
        comment_form = CommentForm(request.data)
        reply_form = ReplyForm(request.data)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.parent_post = blogpost
            new_comment.user = request.user
            new_comment.save()
            # Assuming you have a template for rendering a single comment
            comment_html = render_to_string('comment-partial.html', {'new_comment': new_comment}, request=request)

            return Response({'success': True, 'comment_html': comment_html})

        elif reply_form.is_valid():
            parent_comment_id = request.data.get('parent_comment_id')
            parent_comment = Comment.objects.get(id=parent_comment_id)
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.parent_comment = parent_comment
            new_reply.save()
            return redirect('blog-details', slug=blogpost.slug)

        context = {
            "title": blogpost.title,
            "blogpost": blogpost.serialize(),
            "comments": [comment.serialize() for comment in blogpost.comments.all()],
            'comment_form': comment_form, 
            'reply_form': reply_form,
            'categories': [category.serialize() for category in Category.objects.all()],
            'authors': [author.serialize() for author in Author.objects.all()],
            'latest_posts': [post.serialize() for post in Post.objects.all().order_by('-created')[:3]],
            'previous_page': request.META.get('HTTP_REFERER'),
            'categories_with_post_count': [category.serialize() for category in Category.objects.annotate(post_count=Count('posts'))],
        }

        return Response(context)

@api_view(['GET'])
def search_blogs(request):
    query = request.GET.get('query', '')
    search_results = Post.objects.filter(title__icontains=query) | Post.objects.filter(author__name__icontains=query)

    data = {
        'search_results': [result.serialize() for result in search_results],
        'query': query
    }

    return Response(data)


