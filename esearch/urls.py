from django.urls import path 
from . import views 

app_name = 'esearch' 

urlpatterns = [ 
    path('', views.search_index, name='search_view'), 
    path('blog/',  views.Blog, name='blog'),
    path('blog_search', views.search_blog, name="search_blog")
]