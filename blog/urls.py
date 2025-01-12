from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('pagina_de_acesso/', views.pagina_de_acesso, name="pagina_de_acesso"),
]