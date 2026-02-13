from rest_framework.generics import(
    ListAPIView, CreateAPIView,
    RetrieveUpdateDestroyAPIView

)
from django.db.models import Count, Avg

from .models import Category, Product, Review 
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductReviewSerializer
)


class CategoryListCreateView(ListAPIView, CreateAPIView):
    queryset = Category.objects.annotate(product_count=Count("product"))
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count=Count("product"))
    serializer_class = CategorySerializer
    lookup_field = "id"



class ProductListCreateView(ListAPIView, CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"



class ReviewListCreateView(ListAPIView, CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"




class ProductReviewView(ListAPIView):
    queryset = Product.objects.annotate(rating=Avg("reviews"))
    serializer_class = ProductReviewSerializer