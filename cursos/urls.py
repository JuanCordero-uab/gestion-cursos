from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('crear/', views.crear_curso, name='crear_curso'),
    path('<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('<int:curso_pk>/agregar_material/', views.agregar_material, name='agregar_material'),
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('cursos/<int:curso_id>/inscribirse/', views.inscribirse_curso, name='inscribirse_curso'),
    path('lecciones/<int:leccion_id>/marcar_completada/', views.marcar_completada, name='marcar_completada'),
   
]