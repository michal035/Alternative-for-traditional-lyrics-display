from django.urls import path
from . import views 


urlpatterns = [
    path('upload/<token>/', views.upload_file),
    path('<token>/', views.re),
    path('', views.non),

]