from rest_framework import serializers

from accountapp.models import User

class FriendSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

 