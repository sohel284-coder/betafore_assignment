from django.urls import path

from baseapp.views import PeopleSearchListAPIView


urlpatterns = [
    path('api/people/', PeopleSearchListAPIView.as_view(), name='people_search'),
    
    
]



