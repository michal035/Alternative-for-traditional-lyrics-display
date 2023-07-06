from django.urls import path
from . import views 


urlpatterns = [
    path('upload/<token>/', views.upload_file),
    path('<token>/', views.re),
    path('<token>/qr', views.re_qr),
    path('<token>/check', views.check_for_password),
    path('create-new', views.Create_new_doc),
    path('', views.non),

]