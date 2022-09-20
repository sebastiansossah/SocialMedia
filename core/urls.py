from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('indexfollow/', views.indexfollow, name='indexfollow'),
    path('search/', views.search, name='search'),
    path('settings/', views.settings, name='settings'),
    path('like/', views.like, name='like'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('follows/', views.follows, name='follows'),
    path('profile/<str:pk>', views.theProfile, name='theProfile'),
    path('upload/', views.upload, name='upload'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),

]