from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models import Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer,ProductDetailSerializer, ReviewSerializer, ReviewDetailSerializer,ProductReviewSerializer

# Create your views here.

@api_view(['GET'])
def category_datail_api_views(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.annotate(
        product_count = Count('product')
    )
    data =CategorySerializer(instance=category, many=True).data
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    # step 1: Collect product from DB(QuerySet)
    products = Product.objects.all()
    
    # step 2: Reformat (Serialize) QuerySet to List of dictoinary
    data = ProductSerializer(instance=products, many=True).data
    
    # step 3: Return Response (data, itatus)
    return Response(
        status=status.HTTP_200_OK,
        data=data # dict, list (str, int, float, dict)
    )


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(instance=reviews, many=True).data
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )

@api_view(['GET'])
def product_reviews_api_view(request):
    product = Product.objects.all()
    data = ProductReviewSerializer(product, many=True).data
    avg_rating = Review.objects.aggregate(average_stars=Avg('stars'))['average_stars'] or 0
    return Response(
        status=status.HTTP_200_OK,
        data={
            'products': data,
            'average_stars': round(avg_rating, 2)
        }
    )