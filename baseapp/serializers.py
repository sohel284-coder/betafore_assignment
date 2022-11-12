from rest_framework import serializers

from accountapp.models import User


class PeopleSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', )