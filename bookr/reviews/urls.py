from django.urls import path
from . import views

urlpatterns = [
  path('', views.welcome_view, name='welcome_view'),
  path('books/', views.book_list, name='book_list'),
  path('books/<int:pk>/', views.book_detail, name='book_detail'),
  path('book-search/', views.book_search, name="book_search"),
  path("publishers/<int:pk>/", views.publisher_edit, name="publisher_edit"),
  path("publishers/new/", views.publisher_edit, name="publisher_create"),
  path('books/<int:b_pk>/reviews/new/', views.review_edit, name="review_create"),
  path('books/<int:b_pk>/reviews/<int:r_pk>/', views.review_edit, name="review_edit"),
]