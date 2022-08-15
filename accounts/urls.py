from django.urls import path
from . import views


urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('contactus/', views.contact_us, name='contactus'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('success/', views.success, name='success')
]
