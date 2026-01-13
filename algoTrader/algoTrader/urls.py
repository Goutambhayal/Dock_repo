"""
URL configuration for algoTrader project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from . import views
from .trading_views import (
    trading_interface,
    handle_place_order,
    handle_exit_order,
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('placeOrders.urls')),   #Include the plaeOrders app
    path('', include('users.urls')),  # Include the users app
    path('home/', views.homePage, name='home'),
    path('trading/', trading_interface, name='trading_interface'),
    path('trading/place-order/', handle_place_order, name='place_order'),
    path('trading/exit-order/', handle_exit_order, name='exit_order'),
    #path('trading/modify-order/', handle_modify_order, name='modify_order'),
    #path('trading/delete-order/<int:order_id>/', handle_delete_order, name='delete_order'),
    path('search-scrips/', views.search_scrips, name='search_scrips'),
    path('download-token-list/',views.download_csv,name='download-csv'),
    path('live-price-loop/',views.live_price_loop,name='live_price_loop'),
    path('update-chart-array/<str:token>/',views.update_chart_array,name='update_chart_array'),
    path('holdings/',views.holdings,name='holdings'),
]

