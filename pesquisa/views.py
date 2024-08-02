from django.shortcuts import render

# Create your views here.
# pesquisa/views.py

from django.shortcuts import render, redirect
from .forms import PesquisaForm
from .forms import PrefeitoForm, VereadorForm
from .models import Prefeito

def listar_prefeitos(request):
    prefeitos = Prefeito.objects.all()
    return render(request, 'listar_prefeitos.html', {'prefeitos': prefeitos})

def cadastrar_prefeito(request):
    if request.method == 'POST':
        form = PrefeitoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_prefeitos')  # Redirecione para uma página de sucesso ou lista de prefeitos
    else:
        form = PrefeitoForm()
    return render(request, 'cadastrar_prefeito.html', {'form': form})

def cadastrar_vereador(request):
    if request.method == 'POST':
        form = VereadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_vereadores')  # Redirecione para uma página de sucesso ou lista de vereadores
    else:
        form = VereadorForm()
    return render(request, 'cadastrar_vereador.html', {'form': form})

def pesquisa_create(request):
    if request.method == 'POST':
        form = PesquisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pesquisa_success')
    else:
        form = PesquisaForm()
    return render(request, 'pesquisa/pesquisa_form.html', {'form': form})

def pesquisa_success(request):
    return render(request, 'pesquisa/pesquisa_success.html')
