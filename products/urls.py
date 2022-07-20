from rest_framework. routers import DefaultRouter

from .views import ProductViewSet, CategoryViewSet, CommentViewSet, RatingViewSet

router = DefaultRouter()

router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('comment', CommentViewSet)
router.register('rating', RatingViewSet)

urlpatterns = []
urlpatterns += router.urls
