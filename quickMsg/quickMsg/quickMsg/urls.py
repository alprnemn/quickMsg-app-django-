"""
URL configuration for quickMsg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include

from site_app.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name="homepage"),
    path("login",loginPage,name="login-page"),
    path("signup",signup,name="signup-page"),
    path("logout-page",logoutpage,name="logout-page"),
    path("profile/<userId>",profilePage,name="profile-page"),
    path("profile/<userId>/delete", deleteAccount, name="delete-account"),
    path("profile/<userId>/changeavatar",changeAvatar,name="change-avatar"),
    path("profile/<userId>/follow",followUser,name="follow-user"),
    path("profile/<userId>/unfollow",unfollowUser,name="unfollow-user"),
    path("ban/<userId>", banUser , name="ban-user"),
    path("unban/<userId>",unbanUser,name="unban-user"),
    path("messages/<messageId>", messagePage, name="message-page"),
    path("update/<messageId>",updateMessage , name="update-message"),
    path("messages/delete/<messageId>", deleteMessage, name="delete-message"),
    path("messages/<messageId>/<commentId>", deleteComment, name="delete-comment"),
    path("like/<messageId>",likeView,name="like-post"),
    path("dislike/<messageId>",dislikeView,name="dislike-post"),
    path("promote",promoteToModerator,name="promote"),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
