from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models import Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer,ProductDetailSerializer, ReviewSerializer, ReviewDetailSerializer,ProductReviewSerializer

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
        data = CategoryDetailSerializer(category).data
        return Response(data=data)
    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)
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
        name = request.data.get('name')

        category = Category.objects.create(
            name=name
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)


@api_view(['GET','PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data

    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category = request.data.get('category')
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    # step 1: Collect product from DB(QuerySet)
    if request.method =='GET':
        products = Product.objects.all()
        
        # step 2: Reformat (Serialize) QuerySet to List of dictoinary
        data = ProductSerializer(instance=products, many=True).data
        
        # step 3: Return Response (data, itatus)
        return Response(
            status=status.HTTP_200_OK,
            data=data # dict, list (str, int, float, dict)
        )

    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category=category

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
    data = ReviewDetailSerializer(review, many=False).data

    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.product = request.data.get('product')
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
        data = ReviewSerializer(instance=reviews, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )

    elif request.method == 'POST':
        text = request.data.get('text')
        product_id = request.data.get('product')

        review = Review.objects.create(
            text=text,
            product=product
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