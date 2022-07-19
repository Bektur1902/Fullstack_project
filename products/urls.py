from rest_framework. routers import DefaultRouter

from .views import ProductViewSet, CategoryViewSet, CommentViewSet

router = DefaultRouter()

router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('category', CommentViewSet)

urlpatterns = []
urlpatterns += router.urls
