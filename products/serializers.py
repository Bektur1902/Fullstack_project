from rest_framework import serializers

from .models import Product, Category, CommentAndRating, Favorite, Like


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['like'] = LikeSerializer(instance.like.all(), many=True).data
        rep['favorites'] = FavoritesSerializer(instance.favorites.all(), many=True).data
        rep['rating'] = CommentAndRatingSerializer(instance.comments.all(), many=True).data
        rep['comments'] = CommentAndRatingSerializer(instance.comments.all(), many=True).data

        rating = [dict(i)['rating'] for i in rep['rating']]
        like = sum([dict(i)['like'] for i in rep['like']])
        rep['like'] = like
        favorites = sum([dict(i)['favorites'] for i in rep['favorites']])
        rep['favorites'] = favorites
        if rating:
            rep['rating'] = round((sum(rating) / len(rating)), 2)
            return rep
        else:
            rep['rating'] = None
            return rep


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentAndRatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = CommentAndRating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user
        return super().create(validated_data)


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['author', 'product', 'favorites']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'product', 'like']
