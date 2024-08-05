# coordenador/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Coordenador
from .forms import CoordenadorForm

def coordenador_create(request):
    if request.method == 'POST':
        form = CoordenadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coordenador:coordenador_list')
    else:
        form = CoordenadorForm()
    return render(request, 'coordenador/coordenador_form.html', {'form': form})

def coordenador_update(request, pk):
    coordenador = get_object_or_404(Coordenador, pk=pk)
    if request.method == 'POST':
        form = CoordenadorForm(request.POST, instance=coordenador)
        if form.is_valid():
            form.save()
            return redirect('coordenador:coordenador_list')
    else:
        form = CoordenadorForm(instance=coordenador)
    return render(request, 'coordenador/coordenador_form.html', {'form': form})

def coordenador_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        coordenadores = Coordenador.objects.filter(nome__icontains=search_query)
    else:
        coordenadores = Coordenador.objects.all()
    return render(request, 'coordenador/coordenador_list.html', {'coordenadores': coordenadores})
