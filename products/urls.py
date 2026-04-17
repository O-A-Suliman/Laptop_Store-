from django.urls import path
from .views import ProductsList, ProductDetail, ProductListAPI, ProductDetailAPI,GetDashboard,dashboard_orders_view,complete_order_view,DashboardInventoryView,dashboard_reports_view
from .views import add_to_cart,cart_view,checkout_view,remove_from_cart

urlpatterns = [
    path("", ProductsList.as_view(), name="ProductsList"),
    path("products/<int:pk>/", ProductDetail.as_view(), name='product_detail'),
    path("dashboard/",GetDashboard,name='dashboard'),
    path("dashboard/orders/",dashboard_orders_view,name="dashboard_orders"),
    path("dashboard/orders/complete/<int:order_id>/",complete_order_view,name="complete_order" ),
    path("dashboard/inventory/",DashboardInventoryView.as_view(),name="dashboard_inventory"),
    path("dashboard/reports/",dashboard_reports_view,name='dashboard_reports'),
    path('products/add/<int:product_id>/',add_to_cart,name='add_to_cart'),
    path('products/cartlist/', cart_view, name='cart_view'),
    path('product/checkout/', checkout_view, name='checkout'),
    path('products/cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    path("api/products/", ProductListAPI.as_view(), name="api_products_list"),
    path("api/products/<int:pk>/", ProductDetailAPI.as_view(), name="api_product_detail"),
]