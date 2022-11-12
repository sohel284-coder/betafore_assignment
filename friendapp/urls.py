from django.urls import path

from friendapp.views import *



urlpatterns = [
    path('send-friend-request/<int:userId>/', SendFriendRequestAPIView.as_view(), name='send_friend_request'),
    path('accept-friend-request/<int:requestId>/', AcceptFriendRequestAPIView.as_view(), name='accept_friend_request'),
    path('decline-friend-request/<int:requestId>/', DeclineFriendRequestAPIView.as_view(), name='decline_friend_request'),
    path('my-friend-list/', MyFriendList.as_view(), name='my_friend_list'),

]