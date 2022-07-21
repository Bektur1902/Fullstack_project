from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from .serializers import (
                            ProductSerializer, CategorySerializer,
                            CommentAndRatingSerializer, ProductListSerializer, FavoritesSerializer
)
from .models import Product, Category, CommentAndRating, Like, Favorite
from .filters import ProductsPriceFilter
from .permissions import IsAuthor
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = ProductsPriceFilter
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    @action(['GET'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user

        try:
            like = Like.objects.filter(product_id=product, author=user)
            like_ = not like[0].like
            if like_:
                like[0].save()
            else:
                like.delete()
            message = 'Нравится' if like else 'Не нравится'
        except IndexError:
            Like.objects.create(product_id=product.id, author=user, like=True)
            message = 'Нравится'
        return Response(message, status=200)

    @action(['GET'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            favorites = Favorite.objects.filter(product_id=product, author=user)
            fav_ = not favorites[0].favorites
            if fav_:
                favorites[0].save()
            else:
                favorites.delete()
            message = 'В избранном' if favorites else 'Не в избранном'
        except IndexError:
            Favorite.objects.create(product_id=product.id, author=user, favorites=True)
            message = 'В избранном'
        return Response(message, status=200)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class CommentAndRatingViewSet(ModelViewSet):
    queryset = CommentAndRating.objects.all()
    serializer_class = CommentAndRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


class FavoriteViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]
