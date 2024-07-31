from django.shortcuts import render, get_object_or_404, redirect
from .models import Lideranca, Contato
from .forms import LiderancaForm, ContatoForm

def lideranca_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        liderancas = Lideranca.objects.filter(nome__icontains=search_query)
    else:
        liderancas = Lideranca.objects.all()
    return render(request, 'lideranca/lideranca_list.html', {'liderancas': liderancas})


def lideranca_create(request):
    if request.method == 'POST':
        form = LiderancaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lideranca:lideranca_list')
    else:
        form = LiderancaForm()
    return render(request, 'lideranca/lideranca_form.html', {'form': form})

def lideranca_edit(request, pk):
    lideranca = get_object_or_404(Lideranca, pk=pk)
    if request.method == 'POST':
        form = LiderancaForm(request.POST, instance=lideranca)
        if form.is_valid():
            form.save()
            return redirect('lideranca:lideranca_list')
    else:
        form = LiderancaForm(instance=lideranca)
    return render(request, 'lideranca/lideranca_form.html', {'form': form})

def contato_list(request):
    contatos = Contato.objects.all()
    return render(request, 'lideranca/contato_list.html', {'contatos': contatos})


def contato_create(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lideranca:contato_list')
    else:
        form = ContatoForm()
    return render(request, 'lideranca/contato_form.html', {'form': form})

def contato_edit(request, pk):
    contato = get_object_or_404(Contato, pk=pk)
    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            return redirect('lideranca:contato_list')
    else:
        form = ContatoForm(instance=contato)
    return render(request, 'lideranca/contato_form.html', {'form': form})
