from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('pagina_de_acesso/', views.pagina_de_acesso, name="pagina_de_acesso"),
    path('posts/', views.posts, name="posts"),
    path('deslogar/', views.deslogar, name="deslogar"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)