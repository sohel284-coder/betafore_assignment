from django.shortcuts import render

from rest_framework import filters
from rest_framework.generics import ListAPIView

from accountapp.permissions import CustomPermission
from accountapp.models import User

from baseapp.serializers import PeopleSearchSerializer



class PeopleSearchListAPIView(ListAPIView):
    permission_classes = (CustomPermission, )

    search_fields = ['name', 'email', ]
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = PeopleSearchSerializer