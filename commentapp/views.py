from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from baseapp.base import get_current_user

from postapp.models import Post

from commentapp.models import Comment
from commentapp.serializers import CommentSerializer

from accountapp.permissions import CustomPermission






class CommentAPIView(APIView):
    permission_classes = (CustomPermission, )
    
    def get(self, request, postId):
        current_user = get_current_user(request)
        post = Post.objects.get(pk=postId)
        comments = Comment.objects.filter(post=post, user=current_user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, postId):
        current_user = get_current_user(request)
        post = Post.objects.get(pk=postId)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentUpdateAPIView(APIView):
    permission_classes = (CustomPermission, )


    def get_object(self, postId, commentId, user):
        try:
            return Comment.objects.get(pk=commentId, post=postId, user=user)

        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, postId, commentId):
        user = get_current_user(request)
        comment = self.get_object(postId, commentId, user)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, postId, commentId):
        user = get_current_user(request)
        comment = self.get_object(postId, commentId, user)
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'data':serializer.data,
                'message':'Comment has been updated successfully',
                'status':status.HTTP_201_CREATED
            })
        return Response({
            'data':serializer.errors,
            'message':"Something went wrong",
            'status':status.HTTP_400_BAD_REQUEST
        })


    def delete(self, request, postId, commentId):
        user = get_current_user(request)
        comment = self.get_object(postId, commentId, user)
        comment.delete()
        return Response({
            'data':[],
            'message':"Comment has been deleted successfully",
            'status':status.HTTP_204_NO_CONTENT
        })



class ShowAllCommentsOfPost(APIView):

    permission_classes = (CustomPermission, )
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)