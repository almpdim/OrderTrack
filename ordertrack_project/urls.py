"""
URL configuration for ordertrack_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from ordertrack import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', views.order_list_view, name='order_list'),
    path('track/', views.track_order_view, name='track_order'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('orders/new/', views.order_form_view, name='order_form'),
    path('orders/cancel/', views.order_cancel_view, name='order_cancel'),
    path('orders/status-update/', views.order_status_update_view, name='order_status_update'),
    path('orders/filtered/', views.order_list_filtered_view, name='order_list_filtered'),
    path('orders/sorted/', views.order_list_sorted_view, name='order_list_sorted'),
]
