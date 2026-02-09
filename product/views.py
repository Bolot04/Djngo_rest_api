from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models import Avg
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    CategoryValidateSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ProductValidateSerializer,
    ReviewSerializer,
    ReviewDetailSerializer,
    ReviewValidateSerializer,
    ProductReviewSerializer,
    ProductValidateSerializer
)

# Create your views here.

@api_view(['GET', 'PUT', 'DELETE'])
def category_datail_api_views(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category, many=False).data

    if request.method == 'GET':
        return Response(CategoryValidateSerializer(category).data)

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer = is_valid(raise_exception=True)

        category.name = serializer.validated_data['name']
        category.save()
        return Response(CategoryValidateSerializer(category).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        category = Category.objects.annotate(
            product_count = Count('product')
        )
        data =CategorySerializer(instance=category, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )

    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = Category.objects.create(name=serializer.validated_data['name'])
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)



@api_view(['GET','PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ProductDetailSerializer(product).data)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        product.name = data['name']
        product.title = data['title']
        product.description = data['description']
        product.price = data['price']
        product.category_id = data['category_id']
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    # step 1: Collect product from DB(QuerySet)
    if request.method =='GET':
        products = Product.objects.all()
        
        # step 2: Reformat (Serialize) QuerySet to List of dictoinary
        return Response(ProductSerializer(products, many=True).data)
        
        # step 3: Return Response (data, itatus)
        # return Response(
        #     status=status.HTTP_200_OK,
        #     data=data # dict, list (str, int, float, dict)
        # )

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        product = Product.objects.create(
            name=data['name'],
            title=data['title'],
            description=data['description'],
            price=data['price'],
            category_id=data['category_id']

        )
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ReviewDetailSerializer(review).data)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        review.text = data['text']
        review.product_id = data['product_id']
        review.stars = data.get('stars', review.stars)
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)
                        
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        return Response(ReviewSerializer(instance=reviews, many=True).data)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data        
        review = Review.objects.create(
            text=data['text'],
            product_id=data['product_id'],
            stars=data.get('stars', 5)
        )
        

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)


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