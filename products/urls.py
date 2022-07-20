from rest_framework. routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('comment', CommentAndRatingViewSet)

urlpatterns = []
urlpatterns += router.urls
