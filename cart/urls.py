"""
URL configuration for spare_part_management project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py
from django.urls import path
from .views import AddToCartAPIView
from .views import CartRemoveAPIView
from .views import CartViewAPIView
from .views import CartDeleteAPIView,get_cart_list

urlpatterns = [
    path('add-to-cart/<int:b>/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('cart-remove/<int:b>/', CartRemoveAPIView.as_view(), name='cart_remove'),
    path('cart-view/', CartViewAPIView.as_view(), name='cart_view'),
    path('cart-delete/<int:b>/', CartDeleteAPIView.as_view(), name='cart_delete'),
    path('list/', get_cart_list, name='cart-list')
]


