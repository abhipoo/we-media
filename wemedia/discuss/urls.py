from django.urls import path

from . import views

urlpatterns = [
    path('<int:topic_id>/', views.discuss, name='discuss'),
    path('<int:topic_id>/add_point/', views.add_point, name='add_point'),
    path('<int:topic_id>/add_counterpoint/', views.add_counterpoint, name='add_counterpoint'),
    path('all/', views.show_all_topics, name='all_topics'),
    path('content/<int:content_id>/', views.discuss_content, name='content'),
    path('content/all/', views.show_all_content, name='all_content'),
    ]