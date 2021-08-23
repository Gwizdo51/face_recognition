from django.conf.urls import url
from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.Analyzer.as_view()),
#     # path('', views.upload_img),
#     path('cached_files_cleared/', views.clear_cached_files),
#     path('compute', views.random_int),
#     path('apitest/<username>', views.api_test)
# ]

urlpatterns = [
    path('', views.index),
    path('last_analyzed_image/', views.last_analyzed_image),
    path('cached_files_cleared/', views.clear_cached_files)
]
