from django.urls import path
from . import views
from .feeds import LatestPostFeed

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('feeds/', LatestPostFeed(), name='post_feed'),
    path('<int:year>/<int:month>/<int:day>/' r'<str:post>/', views.post_detail, name='post_detail')
]