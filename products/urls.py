from django.urls import path
from .views import ProductsList, ProductDetail, ProductListAPI, ProductDetailAPI,GetDashborad

urlpatterns = [
    # ---- روابط الموقع العادية (HTML) ----
    path("", ProductsList.as_view(), name="ProductsList"),
    path("products/<int:pk>/", ProductDetail.as_view(), name='product_detail'),
    path("dashborad/",GetDashborad,name='dashborad'),

    # ---- روابط الـ API الجديدة (JSON) ----
    path("api/products/", ProductListAPI.as_view(), name="api_products_list"),
    path("api/products/<int:pk>/", ProductDetailAPI.as_view(), name="api_product_detail"),
]