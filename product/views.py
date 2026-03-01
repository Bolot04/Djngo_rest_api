from rest_framework.generics import(
    ListAPIView, CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)
from rest_framework import generics
from django.db.models import Count, Avg

from .models import Category, Product, Review 
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductReviewSerializer,
    ProductValidateSerializer
)
from cammon.permission import IsModerator
from rest_framework.response import Response
from rest_framework import status

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count("product"))
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count=Count("product"))
    serializer_class = CategorySerializer
    lookup_field = "id"



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsModerator]


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = "id"
    permission_classes = [IsModerator]



class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"


class ProductReviewView(ListAPIView):
    queryset = Product.objects.annotate(rating=Avg("reviews"))
    serializer_class = ProductReviewSerializer