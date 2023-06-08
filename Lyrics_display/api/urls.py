from django.urls import path
from . import views 


urlpatterns = [
    path('upload/', views.upload_file),
    path('<token>/', views.re),
    path('', views.non),

]