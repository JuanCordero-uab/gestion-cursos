from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Curso, MaterialDeApoyo, Inscripcion,Leccion,Progreso
from .forms import CursoForm, MaterialDeApoyoForm
from .emails import enviar_notificacion_inscripcion

def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    return render(request, 'cursos/detalle_curso.html', {'curso': curso})

# Ejemplo de vista para la página de inicio
def inicio(request):
    return render(request, 'inicio.html')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # Reemplaza 'home' con la URL de tu página principal
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

from django.contrib.auth.decorators import login_required

@login_required
def mi_vista_protegida(request):
    if request.user.is_instructor:
        # Lógica para un instructor
        return render(request, 'instructor.html')
    elif request.user.is_student:
        # Lógica para un estudiante
        return render(request, 'estudiante.html')
    else:
        # Otros roles o manejo de errores
        return render(request, 'sin_permisos.html')
    
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.instructor = request.user
            curso.save()
            form.save_m2m()
            return redirect('detalle_curso', pk=curso.pk)
    else:
        form = CursoForm()
    return render(request, 'cursos/crear_curso.html', {'form': form})

@login_required
def detalle_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    return render(request, 'cursos/detalle_curso.html', {'curso': curso})

@login_required
def agregar_material(request, curso_pk):
    curso = Curso.objects.get(pk=curso_pk)
    if request.method == 'POST':
        form = MaterialDeApoyoForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            curso.materiales.add(material)
            return redirect('detalle_curso', pk=curso.pk)
    else:
        form = MaterialDeApoyoForm()
    return render(request, 'cursos/agregar_material.html', {'form': form, 'curso': curso})

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.instructor = request.user
            curso.save()
            form.save_m2m()
            return redirect('detalle_curso', pk=curso.pk)
    else:
        form = CursoForm()
    return render(request, 'cursos/crear_curso.html', {'form': form})

@login_required
def detalle_curso(request, pk):
    curso = Curso.objects.get(pk=pk)
    return render(request, 'cursos/detalle_curso.html', {'curso': curso})

@login_required
def agregar_material(request, curso_pk):
    curso = Curso.objects.get(pk=curso_pk)
    if request.method == 'POST':
        form = MaterialDeApoyoForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            curso.materiales.add(material)
            return redirect('detalle_curso', pk=curso.pk)
    else:
        form = MaterialDeApoyoForm()
    return render(request, 'cursos/agregar_material.html', {'form': form, 'curso': curso})

@login_required
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    usuario = request.user
    inscripcion, created = Inscripcion.objects.get_or_create(usuario=usuario, curso=curso)

    if created:
        # La inscripción fue creada con éxito
        mensaje = "Te has inscrito en el curso exitosamente."
    else:
        # El usuario ya está inscrito en el curso
        mensaje = "Ya estás inscrito en este curso."

    context = {
        'curso': curso,
        'mensaje': mensaje
    }
    return render(request, 'cursos/detalle_curso.html', context)

@login_required
def marcar_completada(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    usuario = request.user
    progreso, created = Progreso.objects.get_or_create(usuario=usuario, leccion=leccion)

    if not progreso.completada:
        progreso.completada = True
        progreso.save()

    return redirect('detalle_curso', pk=leccion.curso.id)

@login_required
def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    lecciones = curso.lecciones.all()
    progreso = Progreso.objects.filter(usuario=request.user, leccion__in=lecciones)

    leccion_progreso = {p.leccion.id: p.completada for p in progreso}

    context = {
        'curso': curso,
        'lecciones': lecciones,
        'leccion_progreso': leccion_progreso,
    }
    return render(request, 'cursos/detalle_curso.html', context)
def progreso_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if curso.instructor != request.user:
        return redirect('lista_cursos')
    
    lecciones = curso.lecciones.all()
    progreso = Progreso.objects.filter(leccion__curso=curso)

    context = {
        'curso': curso,
        'lecciones': lecciones,
        'progreso': progreso,
    }
    return render(request, 'cursos/progreso_curso.html', context)

@login_required
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    usuario = request.user
    curso.usuarios.add(usuario)
    enviar_notificacion_inscripcion(usuario, curso)
    return redirect('detalle_curso', pk=curso.id)