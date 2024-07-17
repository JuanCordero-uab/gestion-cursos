from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    modalidad = models.CharField(max_length=100)  # Ejemplo: "virtual", "presencial"
    tipo = models.CharField(max_length=100)  # Ejemplo: "sincrónico", "asincrónico"
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.DurationField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    materiales = models.ManyToManyField('MaterialDeApoyo', blank=True)

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, related_name='lecciones', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    orden = models.PositiveIntegerField()

    class Meta:
        ordering = ['orden']

class Progreso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.leccion} - {'Completada' if self.completada else 'No completada'}"

class MaterialDeApoyo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='materiales/')
    enlace = models.URLField(blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Inscripcion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"{self.usuario} inscrito en {self.curso}"