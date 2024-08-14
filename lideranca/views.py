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
    # Obtendo o coordenador atual da sessão
    coordenador_id = request.session.get('coordenador_id')
    coordenador = get_object_or_404(Coordenador, pk=coordenador_id)

    # Obtendo o líder associado ao coordenador
    liderancas = Lideranca.objects.filter(coordenador=coordenador)
    lider_ids = liderancas.values_list('id', flat=True)

    # Filtrando contatos vinculados ao líder
    contatos = Contato.objects.filter(lideranca__in=lider_ids)

    # Aplicando a pesquisa, se houver
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
