from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('about.html',views.about,name="about"),
    path('delete/<stock_id>',views.delete,name="delete"),
    path('delete_stock.html',views.delete_stock,name="delete_stock"),
    path('addStock.html',views.addStock,name="addStock"),
    path('visualize.html',views.visualize,name="visualize"),
    path('converter.html',views.converter,name="converter"),
 	path("register/", views.register,name ="register"),
	path("login/",views.userlogin,name="login"),
	path("logout/", views.logoutuser, name ="logout"),

]