from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert, name='convert'),
    path('search/', views.search, name='search'),
    path('update/', views.update_db_with_new_coins,
         name='update_db_with_new_coins')
]
