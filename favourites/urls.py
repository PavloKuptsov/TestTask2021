from rest_framework import routers

from favourites import views

router = routers.DefaultRouter()
router.register(r'favourites', views.FavouritesViewSet, basename='favourites')
router.register(r'tweets', views.TweetsViewSet, basename='tweets')

urlpatterns = router.urls
