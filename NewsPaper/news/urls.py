from django.urls import path
from .views import Posts, SearchPosts, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
#, PostDetail

urlpatterns = [
    path('', Posts.as_view()),
    path('search/', SearchPosts.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('add/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    
]
