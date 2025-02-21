from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('created/<int:order_id>/', views.OrderCreateView.as_view(), name='order_created'),
]