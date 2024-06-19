from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.create_post, name='create-posts'),
    # path('request/posts/', views.create_post_from_request, name='create-requested-posts'),
    path('posts/<int:id>', views.post_detail, name='delete-post'),
    path('section', views.section_posts, name='section-post'),
    path('club/<int:id>/posts', views.club_posts, name='club-post'),
    path('course/<int:id>/posts', views.course_posts, name='course-post'),
    path('general/posts', views.general_posts, name='general-post'),
    path('posts/<int:id>/comments', views.get_or_create_comment, name='create-comment'),
    path('posts/<int:id>/comments/count', views.get_comment_count, name='count-comment'),
    path('comments/<int:id>', views.update_or_delete_comment, name='create-section'),
    path('posts/<int:id>/likes', views.like, name='retrieve-posts'),
    path('posts/<int:id>/unlike', views.unlike, name='retrieve-posts'),
    path('posts/<int:id>/likes/count', views.get_likes_count, name='retrieve-posts'),
    path('request/<int:id>/post', views.create_requested_post, name='create-requested_post'),
    path('posts/trending', views.trending_post, name='trending_post'),
    path('<int:id>/download', views.download_file, name='download_file'),
]