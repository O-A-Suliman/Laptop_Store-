from django.urls import path
from .views import ProductsList,ProductDetail
urlpatterns = [
    path("",ProductsList.as_view(),name="ProductsList"),
    path("products/<int>/",ProductDetail.as_view(),name='ProductDetail'),
]