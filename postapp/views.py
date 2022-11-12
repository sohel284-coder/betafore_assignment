from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from postapp.models import Post, Like
from postapp.serializers import PostSerializer

from baseapp.base import get_current_user

from accountapp.permissions import CustomPermission



class PostAPIView(APIView):
    permission_classes = (CustomPermission, )
    def get(self, request, format=None):
        user = get_current_user(request)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response({
            'data':serializer.data,
            'message':'all posts of current user',
            'status':status.HTTP_200_OK
        })

    def post(self, request, format=None):
        user = get_current_user(request)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({
                'data':serializer.data,
                'message':'Post has been created successfully',
                'status':status.HTTP_201_CREATED
            })
        return Response({
            'data':serializer.errors,
            'message':"Something went wrong",
            'status':status.HTTP_400_BAD_REQUEST
        })



class PostDetail(APIView):
    permission_classes = (CustomPermission, )

    def get_object(self, pk, user):
        try:
            return Post.objects.get(pk=pk, user=user)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = get_current_user(request)
        post = self.get_object(pk, user)
        serializer = PostSerializer(post)
        return Response({
            'data':serializer.data,
            'message':'single post',
            'status':status.HTTP_200_OK
        })


    def put(self, request, pk):
        user = get_current_user(request)
        post = self.get_object(pk, user)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data':serializer.data,
                'message':'Post has been updated successfully',
                'status':status.HTTP_201_CREATED
            })
        return Response({
            'data':serializer.errors,
            'message':"Something went wrong",
            'status':status.HTTP_400_BAD_REQUEST
        })


    def delete(self, request, pk):
        user = get_current_user(request)
        post = self.get_object(pk, user)
        post.delete()
        return Response({
            'data':[],
            'message':"Post has been deleted successfully",
            'status':status.HTTP_204_NO_CONTENT
        })




class MyFriendPostAPIView(APIView):
    permission_classes = (CustomPermission, )

    def get(self, request, format=None):
        current_user = get_current_user(request)
        print(current_user)
        friends = current_user.friends.values_list('id', flat=True)
        print(friends)

        posts = Post.objects.filter(user__in=list(friends))
        print(posts)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeAPIView(APIView):
    permission_classes = (CustomPermission, )

    def get(self, request, postId):
        current_user = get_current_user(request)
        post = Post.objects.get(pk=postId)
        already_liked = Like.objects.filter(post=post, user=current_user)
        if not already_liked:
            post_liked = Like(post=post, user=current_user)
            post_liked.save()
            post.liked = True
            post.save()
            return Response('Post has been liked')
        return Response("Post has been already liked")


class UnlikeAPIView(APIView):
    permission_classes = (CustomPermission, )

    def get(self, request, postId):
        current_user = get_current_user(request)
        post = Post.objects.get(pk=postId)
        already_liked = Like.objects.filter(post=post, user=current_user)
        already_liked.delete()
        return Response('Post has been unliked successfully')


