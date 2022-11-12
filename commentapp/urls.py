from django.urls import path

from commentapp.views import *


urlpatterns = [
    path('<int:postId>/', CommentAPIView.as_view(), name='comment'),
    path('<int:postId>/<int:commentId>/', CommentUpdateAPIView.as_view(), name='single-comment'),
    path('all/', ShowAllCommentsOfPost.as_view(), name='show_all_comments'),

]
