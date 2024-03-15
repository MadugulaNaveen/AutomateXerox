from django.urls import path
from . import views

urlpatterns = [
  path('', views.load, name='load'),
  path('register', views.register, name='register'),
  path('login',views.login,name='login'),
  path('xerox_details',views.xerox_details,name='xerox_details'),
  path('calculate/<int:order_id>/', views.calculate, name='calculate'),
  path('orders',views.orders, name = 'orders'),
  path('update',views.update,name = 'update'),
 path('delete_row/<int:order_id>/', views.delete_row, name='delete_row'),
 path('payment_verification/<int:order_id>/', views.payment_verification, name='payment_verification'),
]