from django.urls import path
from products import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/<int:product_pk>/files/', views.FileListView.as_view(), name='files_list'),
    path('products/<int:product_pk>/files/<int:pk>/', views.FileDetailView.as_view(), name='file_detail'),
]