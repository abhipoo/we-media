from django.urls import path

from . import views

urlpatterns = [
    path('<int:topic_id>/', views.discuss, name='discuss'),
    #path('<int:topic_id>/add_point/', views.add_point, name='add_point'),
    #path('<int:topic_id>/add_counterpoint/', views.add_counterpoint, name='add_counterpoint'),
    path('all/', views.show_all_topics, name='all_topics'),
    path('content/<int:content_id>/', views.view_content, name='content'),
    path('content/all/', views.show_all_content, name='all_content'),
    path('ask/<int:ask_id>/', views.view_ask, name='ask'),
    path('ask/<int:ask_id>/add_suggestion/', views.add_suggestion, name='add_suggestion'),
    path('discussion/<int:comment_id>/', views.view_discussion, name='discussion'),
    path('discussion/<int:comment_id>/add_point/', views.add_point, name='add_point'),
    path('discussion/<int:comment_id>/add_counterpoint/', views.add_counterpoint, name='add_counterpoint'),
    ]