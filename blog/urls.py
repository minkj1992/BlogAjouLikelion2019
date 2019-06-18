"""blog2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
import blog.views
from django.conf.urls import url

app_name = 'blog'
urlpatterns = [
    # path('', blog.views.notice, name ='notice'),
    # path('<int:pk>/', blog.views.post_read, name='read'),
    # path('create/', blog.views.post_create, name='create'),
    # path('edit/<int:pk>/', blog.views.post_edit, name='edit'),
    # path('update/<int:pk>/', blog.views.post_update, name='update'),
    # path('destroy/<int:pk>/', blog.views.post_destroy, name='destroy'),
# 이게 처음 웹페이지여야한다.
    # url(r'^boards/$', blog.views.board, name='boards'),
    # url(r'^boards/(?P<pk>\d+)/$', blog.views.board_topics, name='board_topics'),
    # url(r'^boards/(?P<pk>\d+)/new/$', blog.views.new_topic, name='new_topic'),
    path('boards/',blog.views.BoardListView.as_view(), name ='boards'),
    path('boards/<int:pk>/', blog.views.TopicListView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', blog.views.new_topic, name='new_topic'),
    
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', blog.views.PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', blog.views.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        blog.views.PostUpdateView.as_view(), name='edit_post'),
    # path('boards/<int:pk>/topics/<int:topic_pk>/', blog.views.topic_posts, name='topic_posts'),
    
]
