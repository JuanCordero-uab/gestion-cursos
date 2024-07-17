from celery import shared_task
from .emails import enviar_recordatorio_curso, enviar_actualizacion_materiales
from .models import Curso

@shared_task
def enviar_recordatorio():
    cursos = Curso.objects.filter(fecha__gte=timezone.now(), fecha__lte=timezone.now() + timedelta(days=1))
    for curso in cursos:
        for usuario in curso.usuarios.all():
            enviar_recordatorio_curso(usuario, curso)

@shared_task
def enviar_actualizaciones_materiales(curso_id):
    curso = Curso.objects.get(id=curso_id)
    for usuario in curso.usuarios.all():
        enviar_actualizacion_materiales(usuario, curso)