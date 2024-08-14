# coordenador/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Coordenador
from .forms import CoordenadorForm
from lideranca.models import Contato
from django.contrib import messages

import base64
import io
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Count
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            try:
                coordenador = Coordenador.objects.get(usuario=usuario, senha=senha)
                # Armazenar o ID do coordenador na sessão
                request.session['coordenador_id'] = coordenador.id
                return redirect('coordenador:coordenador_main', coordenador_id=coordenador.id)  # Redireciona para a tela principal1
            except Coordenador.DoesNotExist:
                messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = LoginForm()
    return render(request, 'coordenador/login.html', {'form': form})


def coordenador_main(request, coordenador_id):
    coordenador = get_object_or_404(Coordenador, pk=coordenador_id)

    # Filtre os contatos pela liderança associada ao coordenador
    contatos = Contato.objects.filter(lideranca__coordenador=coordenador)
    total_contatos = contatos.count()

    contact_graph, _ = generate_contact_graph(contatos)
    city_graph, _ = generate_city_graph(contatos)

    # Calcule a contagem de contatos por bairro
    bairros_contagem = contatos.values('bairro').annotate(contagem=Count('bairro'))
    bairros_percentuais = [
        {
            'nome': bairro['bairro'],
            'contagem': bairro['contagem'],
            'percentual': (bairro['contagem'] / total_contatos) * 100
        }
        for bairro in bairros_contagem
    ]

    # Calcule a contagem de contatos por cidade
    cidades_contagem = contatos.values('cidade').annotate(contagem=Count('cidade'))
    cidades_percentuais = [
        {
            'nome': cidade['cidade'],
            'contagem': cidade['contagem'],
            'percentual': (cidade['contagem'] / total_contatos) * 100
        }
        for cidade in cidades_contagem
    ]

    return render(request, 'coordenador/principal1.html', {
        'contact_graph': contact_graph,
        'city_graph': city_graph,
        'total_contacts': total_contatos,
        'bairros': sorted(bairros_percentuais, key=lambda x: x['percentual'], reverse=True),
        'cidades': sorted(cidades_percentuais, key=lambda x: x['percentual'], reverse=True),
    })

def generate_contact_graph(contatos):
    total_contatos = contatos.count()

    if total_contatos == 0:
        return "", total_contatos

    lideranca_counts = contatos.values('lideranca__nome').annotate(count=Count('lideranca'))
    labels = [l['lideranca__nome'] for l in lideranca_counts]
    sizes = [l['count'] for l in lideranca_counts]

    # Gerar cores distintas
    num_colors = len(labels)
    colors = plt.cm.viridis(np.linspace(0, 1, num_colors))

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, sizes, color=colors, edgecolor='black')

    ax.set_xlabel('Liderança')
    ax.set_ylabel('Contagem')
    ax.set_title('Contagem de Contatos por Liderança')
    ax.set_xticklabels(labels, rotation=45, ha='right')

    # Ajuste de layout
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64, total_contatos

def generate_city_graph(contatos):
    total_contatos = contatos.count()

    if total_contatos == 0:
        return "", total_contatos

    cidades_contagem = contatos.values('cidade').annotate(contagem=Count('cidade'))
    cidades = [cidade['cidade'] for cidade in cidades_contagem]
    contagens = [cidade['contagem'] for cidade in cidades_contagem]

    # Gerar cores distintas
    num_colors = len(cidades)
    colors = plt.cm.tab10(np.linspace(0, 1, num_colors))

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(cidades, contagens, color=colors, edgecolor='black')

    ax.set_xlabel('Cidade')
    ax.set_ylabel('Número de Contatos')
    ax.set_title('Número de Contatos por Cidade')

    # Adiciona valores acima das barras
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom', ha='center')

    # Ajuste de layout
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64, total_contatos

def principal1_view(request):
    coordenador_id = request.session.get('coordenador_id')
    if coordenador_id is None:
        return redirect('login')  # Redireciona para a página de login se não estiver autenticado

    coordenador = Coordenador.objects.get(id=coordenador_id)
    # Aqui, você pode incluir a lógica para obter dados específicos para a página principal1

    context = {
        'coordenador': coordenador,
        # Adicione mais dados ao contexto conforme necessário
    }
    return render(request, 'coordenador/principal1.html', context)

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
