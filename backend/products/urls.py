from django.urls import path
from . import views

urlpatterns = [
    # Add a URL pattern that maps to the RetrieveAPIView
    path('', views.product_list_create_view),
    path('<int:pk>/', views.product_detail_view),
    path('<int:pk>/update/', views.product_update_view),
    path('<int:pk>/destroy/', views.product_destroy_view),


]