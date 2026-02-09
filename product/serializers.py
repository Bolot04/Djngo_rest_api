from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = 'id name product_count'.split()

 
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'stars']

class ProductSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'reviews']
        depth = 1
        # fields = 'id title description price category'.split()
        # fields ='__all__'
        # exclude = 'category price'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title reviews rating'.split()

    def get_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 2) if avg else 0


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=50)


class ProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=50)
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(default='No description')
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError('Category not found!')
        return value


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=2, default='NO text')
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, default=5)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product not found!")
        return value