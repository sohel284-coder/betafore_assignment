from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accountapp.models import User
from accountapp.permissions import CustomPermission

from baseapp.base import get_current_user

from friendapp.models import FriendRequest
from friendapp.serializers import FriendSerializer



class SendFriendRequestAPIView(APIView):
    permission_classes = (CustomPermission, )
    def get(self, request, userId):
        from_user = get_current_user(request)
        to_user = User.objects.get(id=userId)
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        print(friend_request)
        print(created)
        if created:
            return Response('Friend request sent')
        
        return Response('Friend request was already sent')



class AcceptFriendRequestAPIView(APIView):

    permission_classes = (CustomPermission, )
    def get(self, request, requestId):
        current_user = get_current_user(request)
        try:
            friend_request = FriendRequest.objects.get(id=requestId)
            print(friend_request.from_user.friends)
        except FriendRequest.DoesNotExist: 
            raise Http404
        
        if friend_request.to_user == current_user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return Response('friend request accepted')

        return Response('friend request not accepted')



class DeclineFriendRequestAPIView(APIView):

    permission_classes = (CustomPermission, )
    def get(self, request, requestId):
        try:
            friend_request = FriendRequest.objects.get(id=requestId)
            
            print(friend_request.from_user.friends)
        except FriendRequest.DoesNotExist: 
            raise Http404

        friend_request.delete()
        
        return Response('friend request not accepted')


class MyFriendList(APIView):
    permission_classes = (CustomPermission, )
    def get(self, request, format=None):
        user = get_current_user(request)
        friends = user.friends.all()
        friend_list = []

        for friend in friends:
            friend_dict = {}
            friend_dict['name'] = friend.name
            friend_dict['email'] = friend.email
            friend_list.append(friend_dict)
        
        serializer = FriendSerializer(friend_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)