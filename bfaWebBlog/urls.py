from django.urls import path
from django.contrib.auth.views import LogoutView
from bfaWebBlog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('blog-details/<slug>', views.blogDetails, name="blog-details"),
    path('reply/<uuid:comment_id>', views.reply_comment, name="reply"),        
    path('search/', views.searchblogs, name='search'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout')
]