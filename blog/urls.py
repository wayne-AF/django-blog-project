from . import views
from django.urls import path


urlpatterns = [
    # because we're using class-based views, we need to add as_view() to PostList so it will render this class as a view
    path('', views.PostList.as_view(), name='home'),
    # slug keyword matches slug parameter in the get method of the PostDetail class in views.py. This is how we link them?
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
]