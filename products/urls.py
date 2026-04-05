from django.urls import path
from .views import ProductsList,ProductDetail
urlpatterns = [
    path("",ProductsList.as_view(),name="ProductsList"),
    path("products/<int:pk>/", ProductDetail.as_view(), name='product_detail'),
]