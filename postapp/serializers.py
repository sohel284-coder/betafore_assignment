from rest_framework import serializers

from postapp.models import Post



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('body', )



