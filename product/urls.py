from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailView.as_view()),
    path('products/', views.ProductListCreateView.as_view()),
    path('products/<int:id>/', views.ProductDetailView.as_view()),
    path('reviews/', views.ReviewListCreateView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailView.as_view()),
    path('products/reviews/', views.ProductReviewView.as_view())
]