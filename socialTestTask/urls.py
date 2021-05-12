from django.conf.urls import url
from django.urls import path, include


urlpatterns = [
    url('', include('favourites.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
