
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def enviar_notificacion_inscripcion(usuario, curso):
    subject = f'Inscripción en el curso {curso.titulo}'
    html_message = render_to_string('emails/inscripcion.html', {'usuario': usuario, 'curso': curso})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = usuario.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def enviar_recordatorio_curso(usuario, curso):
    subject = f'Recordatorio: Curso {curso.titulo} pronto comenzará'
    html_message = render_to_string('emails/recordatorio.html', {'usuario': usuario, 'curso': curso})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = usuario.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def enviar_actualizacion_materiales(usuario, curso):
    subject = f'Actualización de materiales en el curso {curso.titulo}'
    html_message = render_to_string('emails/actualizacion.html', {'usuario': usuario, 'curso': curso})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = usuario.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
