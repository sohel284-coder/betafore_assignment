from django.urls import path

from postapp.views import *


urlpatterns = [
    path('', PostAPIView.as_view(), name='post_create_view'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail_update_delete'),

    path('my-friend-post/', MyFriendPostAPIView.as_view(), name='my_friend_post'),

    path('like/<int:postId>/', LikeAPIView.as_view(), name='like'),
    path('unlike/<int:postId>/', UnlikeAPIView.as_view(), name='unlike'),


]