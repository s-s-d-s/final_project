from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.BaseView.as_view(), name="home"),
    path('create/', views.CreatePost.as_view(), name="create"),
    path('post/<int:pk>/', views.PostCheck.as_view(), name="postcheck"),
    path('search/', views.Search.as_view(), name="search"),
    path('like/', views.like_dislike, name="like"),
    path('edit/<int:pk>/', views.PostEdit.as_view(), name="post_edit"),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name="post_delete"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)