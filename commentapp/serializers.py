from rest_framework import serializers
from commentapp.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('body', )
        