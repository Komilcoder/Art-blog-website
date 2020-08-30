from django.urls import path
from .views import post_commentview,like_unlike_post,PostDeleteView,PostUpdateView

app_name = 'posts'
urlpatterns = [
    path('', post_commentview, name="post_comment_view"),
    path('like/', like_unlike_post, name="like-post"),
    path('<pk>/delete/',PostDeleteView.as_view(), name="post-delete"),
    path('<pk>/update/',PostUpdateView.as_view(), name="post-update"),
]
