from django.urls import path

from . import views

urlpatterns = [
    path('<int:topic_id>/', views.view_topic, name='view_topic'),
    path('all/', views.show_all_topics, name='all_topics'),
    path('content/<int:content_id>/', views.view_content, name='content'),
    path('content/all/', views.show_all_content, name='all_content'),
    path('ask/<int:ask_id>/', views.view_ask, name='ask'),
    path('ask/<int:ask_id>/add_suggestion/', views.add_suggestion, name='add_suggestion'),
    path('ask/all/', views.show_all_asks, name='all_asks'),
    path('discussion/<int:comment_id>/', views.view_discussion, name='discussion'),
    path('discussion/<int:comment_id>/add_point/', views.add_point, name='add_point'),
    path('discussion/<int:comment_id>/add_counterpoint/', views.add_counterpoint, name='add_counterpoint'),
    path('discussion/all/', views.show_all_discussions, name='all_discussions'),
    path('<int:topic_id>/create_discussion/', views.create_discussion_on_topic, name='create_discussion_on_topic'),
    path('content/<int:content_id>/create_discussion/', views.create_discussion_on_content, name='create_discussion_on_content'),
    ]