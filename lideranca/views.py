from django.shortcuts import render, get_object_or_404, redirect
from .models import Lideranca, Contato
from .forms import LiderancaForm, ContatoForm
from datetime import datetime
from .utils import aniversariantes_do_mes_atual_e_seguinte
from .forms import RelatorioForm
from django.db.models import Count
from .forms import QRCodeForm
from django.urls import reverse
from .models import Lideranca, Coordenador
from lideranca.models import Contato
from .models import Lideranca, Coordenador, Contato

from .forms import LoginForm
from django.contrib import messages
import base64
import io
import matplotlib.pyplot as plt
import numpy as np

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            try:
                lideranca = Lideranca.objects.get(usuario=usuario, senha=senha)
                # Armazenar o ID da liderança na sessão
                request.session['lideranca_id'] = lideranca.id
                return redirect('lideranca:lideranca_main', lideranca_id=lideranca.id)  # Redireciona para a tela principal
            except Lideranca.DoesNotExist:
                messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = LoginForm()
    return render(request, 'lideranca/login.html', {'form': form})


def lideranca_main(request, lideranca_id):
    lideranca = get_object_or_404(Lideranca, pk=lideranca_id)

    # Filtre os contatos pela liderança associada ao coordenador
    contatos = Contato.objects.filter(lideranca=lideranca)
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

    return render(request, 'lideranca/principal2.html', {
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

def generate_qr_code(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            link_choice = form.cleaned_data['link']
            # Mapeie as escolhas para URLs reais
            url_mapping = {
                'coordenador': 'coordenador:coordenador_list',
                'lideranca': 'lideranca:lideranca_list',
                'contato': 'lideranca:contato_list',
            }
            # Verifique se a escolha do link é válida
            if link_choice in url_mapping:
                url_name = url_mapping[link_choice]
                # Gere a URL completa
                link = request.build_absolute_uri(reverse(url_name))
                return render(request, 'generate_qr_code.html', {'form': form, 'qr_code_link': link})
            else:
                # Caso o link_choice não esteja no mapeamento, trate o erro
                form.add_error('link', 'Escolha inválida.')
    else:
        form = QRCodeForm()

    return render(request, 'generate_qr_code.html', {'form': form})


def relatorio_cadastros(request):
    form = RelatorioForm(request.POST or None)
    resultados = None
    
    if request.method == 'POST' and form.is_valid():
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']
        nome_lideranca = form.cleaned_data['nome_lideranca']
        
        # Filtra os cadastros da liderança no período especificado
        query = Lideranca.objects.filter(
            data_nascimento__range=[data_inicio, data_fim]
        )
        
        if nome_lideranca:
            query = query.filter(nome__icontains=nome_lideranca)
        
        resultados = query.values('nome').annotate(num_cadastros=Count('id')).order_by('nome')
    
    return render(request, 'relatorio_cadastros.html', {
        'form': form,
        'resultados': resultados
    })


def relatorio_aniversariantes(request):
    liderancas, contatos = aniversariantes_do_mes_atual_e_seguinte()
    hoje = datetime.now()
    mes_atual = hoje.month
    mes_seguinte = mes_atual + 1 if mes_atual < 12 else 1
    
    context = {
        'liderancas': liderancas,
        'contatos': contatos,
        'mes_atual': mes_atual,
        'mes_seguinte': mes_seguinte,
    }
    
    return render(request, 'relatorio_aniversariantes.html', context)


def lideranca_list(request):
    # Obtendo o coordenador atual da sessão
    coordenador_id = request.session.get('coordenador_id')
    coordenador = get_object_or_404(Coordenador, pk=coordenador_id)

    # Filtrando lideranças vinculadas ao coordenador
    liderancas = Lideranca.objects.filter(coordenador=coordenador)

    # Aplicando a pesquisa, se houver
    search_query = request.GET.get('search', '')
    if search_query:
        liderancas = liderancas.filter(nome__icontains=search_query)

    context = {
        'liderancas': liderancas,
    }
    return render(request, 'lideranca/lideranca_list.html', context)


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
    # Obtém o ID do usuário logado
    lideranca_id = request.session.get('lideranca_id')
    coordenador_id = request.session.get('coordenador_id')
    candidato_id = request.session.get('candidato_id')

    if lideranca_id:
        # Usuário é da Liderança
        lideranca = get_object_or_404(Lideranca, pk=lideranca_id)
        contatos = Contato.objects.filter(lideranca=lideranca)
    elif coordenador_id:
        # Usuário é Coordenador
        coordenador = get_object_or_404(Coordenador, pk=coordenador_id)
        contatos = Contato.objects.filter(coordenador=coordenador)
    elif candidato_id:
        # Usuário é Candidato
        contatos = Contato.objects.all()
    else:
        # Usuário não autenticado
        messages.error(request, "Usuário não autenticado.")
        return redirect('login')  # Redireciona para a página de login ou outra apropriada

    # Aplicar filtro de pesquisa se houver, exceto para o tipo Candidato
    if candidato_id:
        # Para candidatos, não aplicamos filtro de pesquisa
        pass
    else:
        search_query = request.GET.get('search', '')
        if search_query:
            contatos = contatos.filter(nome__icontains=search_query)

    context = {
        'contatos': contatos,
    }
    return render(request, 'lideranca/contato_list.html', context)



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
