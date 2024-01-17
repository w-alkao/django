from django.urls import path
from . import views

urlpatterns = [
  path('', views.welcome_view, name='welcome_view'),
  path('books/', views.book_list, name='book_list'),
]