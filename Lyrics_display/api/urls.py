from django.urls import path
from . import views 


urlpatterns = [
    path('upload/<token_>/', views.upload_file),
    path('<token>/', views.re),
    path('<token>/qr', views.get_qr),
    path('create-new', views.Create_new_doc),
    path("login", views.login),
    path('create-account', views.create_new_account),
    path('', views.non),

]