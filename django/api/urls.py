from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<str:category_name>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),

    path('categoryregions/', views.CategoryRegionListCreateAPIView.as_view(), name='category-region-list'),
    path('categoryregions/<str:region>/', views.CategoryRegionDetailAPIView.as_view(), name='category-region-detail'),

    path('autos/', views.AutoListCreateAPIView.as_view(), name='auto-list'),
    path('autos/<str:car_id>/', views.AutoDetailAPIView.as_view(), name='auto-detail'),

    path('parkings/', views.ParkingCreateAPIView.as_view(), name='parking-list'),
    path('parkings/<int:parking_count>/', views.ParkingDetailAPIView.as_view(), name='parking-detail'),
]
