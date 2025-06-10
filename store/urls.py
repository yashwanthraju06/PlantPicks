from django.contrib import admin
from django.urls import path, include
from . import views
from .views import update_password_view

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='Register'),
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:foo>',views.category,name='category'),
    path('category_summary/',views.category_summary,name='category_summary'),
    path('update_user/',views.update_user,name='update_user'),
    path('update-password/', update_password_view, name='update_password'),
    path('update_info/',views.update_info,name='update_info'),
    path('search/',views.search,name='search'),
]