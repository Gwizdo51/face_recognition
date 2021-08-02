from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Analyzer.as_view()),
    # path('', views.upload_img),
    path('show_uploaded_image/', views.test_show_lastest_uploaded_image),
    path('compute', views.random_int),
    path('apitest/<username>', views.api_test)
]