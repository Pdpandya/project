from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('signin/', views.signin, name='signin'),
    path('login/', views.login, name='login'),  
    path('logout/', views.logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('shop/', views.shop, name='shop'),
    path('cpass/', views.cpass, name='cpass'),
    path('fpass/', views.fpass, name='fpass'),
    path('otp/', views.otp, name='otp'),
    path('newpassword/', views.newpassword, name='newpassword'),
    path('uprofile/', views.uprofile, name='uprofile'),
    path('sindex/', views.sindex, name='sindex'),
    path('sprofile/', views.sprofile, name='sprofile'),
    path('scontact/', views.scontact, name='scontact'),
    path('sabout/', views.sabout, name='sabout'),
    path('snewpassword/', views.snewpassword, name='snewpassword'),
    path('sadd/', views.sadd, name='sadd'),
    path('sview/', views.sview, name='sview'),
    path('pdetails/<int:pk>/', views.pdetails, name='pdetails'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('pdelete/<int:pk>/', views.pdelete, name='pdelete'),
    path('bdetails/<int:pk>/', views.bdetails, name='bdetails'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('addwish/<int:pk>/', views.addwish, name='addwish'),
    path('wishdelete/<int:pk>/', views.wishdelete, name='wishdelete'),
    path('cart/', views.cart, name='cart'),
    path('addcart/<int:pk>/', views.addcart, name='addcart'),
    path('cartdelete/<int:pk>/', views.cartdelete, name='cartdelete'),
    path('changeqty/<int:pk>', views.changeqty, name='changeqty'),
    path('sucess/',views.sucess,name='sucess'),
    path('myorder/',views.myorder,name='myorder'),
    
]


