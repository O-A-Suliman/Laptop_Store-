from django.urls import path
from .views import ProductsList, ProductDetail, ProductListAPI, ProductDetailAPI,GetDashboard,dashboard_orders_view,complete_order_view,DashboardInventoryView,dashboard_reports_view

urlpatterns = [
    # ---- روابط الموقع العادية (HTML) ----
    path("", ProductsList.as_view(), name="ProductsList"),
    path("products/<int:pk>/", ProductDetail.as_view(), name='product_detail'),
    path("dashboard/",GetDashboard,name='dashboard'),
    path("dashboard/orders/",dashboard_orders_view,name="dashboard_orders"),
    path("dashboard/orders/complete/<int:order_id>/",complete_order_view,name="complete_order" ),
    path("dashboard/inventory/",DashboardInventoryView.as_view(),name="dashboard_inventory"),
    path("dashboard/reports/",dashboard_reports_view,name='dashboard_reports'),

    # ---- روابط الـ API الجديدة (JSON) ----
    path("api/products/", ProductListAPI.as_view(), name="api_products_list"),
    path("api/products/<int:pk>/", ProductDetailAPI.as_view(), name="api_product_detail"),
]