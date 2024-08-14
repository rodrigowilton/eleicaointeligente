# coordenador/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Coordenador
from .forms import CoordenadorForm
from lideranca.models import Contato

import base64
import io
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Count


def coordenador_main(request):
    contact_graph, total_contacts = generate_contact_graph()
    city_graph, _ = generate_city_graph()  # Inclua o total_contatos se necessário

    # Obtenha todos os contatos
    contatos = Contato.objects.all()

    # Calcule o total de contatos
    total_contatos = contatos.count()

    # Calcule a contagem de contatos por bairro
    bairros_contagem = contatos.values('bairro').annotate(contagem=Count('bairro'))

    # Calcule a porcentagem de contatos por bairro
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

    # Calcule a porcentagem de contatos por cidade
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
        'total_contacts': total_contacts,
        'bairros': sorted(bairros_percentuais, key=lambda x: x['percentual'], reverse=True),
        'cidades': sorted(cidades_percentuais, key=lambda x: x['percentual'], reverse=True),
    })

def generate_contact_graph():
    contatos = Contato.objects.all()
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

def generate_city_graph():
    contatos = Contato.objects.all()
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
