from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidato, Meta, StatusContato
from .forms import CandidatoForm, MetaForm, StatusForm
import io
import base64
from lideranca.models import Contato
from django.db.models import Count
import numpy as np
import pywhatkit as kit
from pywhatkit.whats import sendwhats_image, sendwhatmsg
from django.contrib import messages
import os
from django.conf import settings
import logging
import time
import pyautogui
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)

def send_whatsapp_message(request):
    if request.method == 'POST':
        message_body = request.POST.get('message_body', '').strip()
        image = request.FILES.get('image')
        document = request.FILES.get('document')

        if not message_body and not image and not document:
            messages.error(request, 'A mensagem não pode estar vazia e deve incluir um anexo ou texto.')
            return redirect('candidato:send_whatsapp_message')

        contatos = Contato.objects.filter(msg=True)
        if not contatos.exists():
            messages.info(request, 'Nenhum contato marcado para envio de mensagem.')
            return redirect('candidato:send_whatsapp_message')

        try:
            for contato in contatos:
                telefone_completo = f"+55{contato.telefone}".replace(" ", "").replace("-", "")
                logger.info(f"Enviando mensagem para contato: {contato.nome} - {telefone_completo}")

                """# Abre o navegador e vai para o WhatsApp Web
                pyautogui.hotkey('ctrl', 't')
                pyautogui.write('https://web.whatsapp.com')
                pyautogui.press('enter')
                time.sleep(40)  # Aguarda o carregamento da página """

                # Pesquisa e seleciona o contato
                pyautogui.click(x=230, y=181)  # Coordenada para a caixa de pesquisa
                time.sleep(2)
                pyautogui.write(telefone_completo)
                time.sleep(2)
                pyautogui.press('enter')
                time.sleep(10)  # Aguarda a abertura do chat

                # Envia a mensagem
                pyautogui.write(message_body)
                pyautogui.press('enter')
                logger.info(f"Mensagem enviada para {contato.nome}: {message_body}")

                if image:
                    image_path = os.path.join(settings.MEDIA_ROOT, image.name)
                    with open(image_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)

                    pyautogui.click(x=700, y=978)  # Coordenada para o botão de anexo
                    time.sleep(2)
                    pyautogui.click(x=772, y=764)  # Coordenada para o botão de imagem
                    time.sleep(2)
                    pyautogui.write(image_path)
                    pyautogui.press('enter')
                    time.sleep(2)
                    pyautogui.press('enter')
                    logger.info(f"Imagem enviada para {contato.nome}: {image.name}")

                if document:
                    document_path = os.path.join(settings.MEDIA_ROOT, document.name)
                    with open(document_path, 'wb+') as destination:
                        for chunk in document.chunks():
                            destination.write(chunk)

                    pyautogui.click(x=700, y=978)  # Coordenada para o botão de anexo
                    time.sleep(2)
                    pyautogui.click(x=781, y=721)  # Coordenada para o botão de documento
                    time.sleep(2)
                    pyautogui.write(document_path)
                    pyautogui.press('enter')
                    time.sleep(2)
                    pyautogui.press('enter')
                    logger.info(f"Documento enviado para {contato.nome}: {document.name}")

                contato.msg = False
                contato.save()
            messages.success(request, 'Mensagens enviadas com sucesso!')
        except Exception as e:
            logger.error(f'Erro ao enviar mensagens: {e}', exc_info=True)
            messages.error(request, f'Erro ao enviar mensagens: {e}')

        # Fecha a aba do navegador com WhatsApp Web
        time.sleep(5)  # Aguarda o fechamento da aba
        """pyautogui.hotkey('ctrl', 'w')
        time.sleep(1)  # Aguarda o fechamento da aba
        pyautogui.press('enter')
        time.sleep(1)  # Aguarda o fechamento da aba
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(5)  # Aguarda o fechamento da aba
        pyautogui.press('f5')"""

        return render(request, 'candidato/send_whatsapp_message.html')

    contatos = Contato.objects.all()
    return render(request, 'candidato/send_whatsapp_message.html', {'contatos': contatos})


def mark_all_contacts(request):
    if request.method == 'POST':
        Contato.objects.update(msg=True)
        messages.success(request, 'Todos os contatos foram marcados para envio de mensagem.')
    return redirect('candidato:send_whatsapp_message')

def mark_selected_contacts(request):
    if request.method == 'POST':
        selected_contacts = request.POST.getlist('selected_contacts')
        Contato.objects.filter(id__in=selected_contacts).update(msg=True)
        messages.success(request, 'Contatos selecionados foram marcados para envio de mensagem.')
    return redirect('candidato:send_whatsapp_message')

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

def index(request):
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

    return render(request, 'principal.html', {
        'contact_graph': contact_graph,
        'city_graph': city_graph,
        'total_contacts': total_contacts,
        'bairros': sorted(bairros_percentuais, key=lambda x: x['percentual'], reverse=True),
        'cidades': sorted(cidades_percentuais, key=lambda x: x['percentual'], reverse=True),
    })

def meta_create(request):
    if request.method == 'POST':
        form = MetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidato:meta_list')
    else:
        form = MetaForm()
    return render(request, 'candidato/meta_form.html', {'form': form})

def meta_list(request):
    metas = Meta.objects.all()
    return render(request, 'candidato/meta_list.html', {'metas': metas})

def meta_edit(request, pk):
    meta = get_object_or_404(Meta, pk=pk)
    if request.method == 'POST':
        form = MetaForm(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            return redirect('candidato:meta_list')
    else:
        form = MetaForm(instance=meta)
    return render(request, 'candidato/meta_form.html', {'form': form})

def meta_delete(request, pk):
    meta = get_object_or_404(Meta, pk=pk)
    if request.method == 'POST':
        meta.delete()
        return redirect('candidato:meta_list')
    return render(request, 'candidato/meta_confirm_delete.html', {'meta': meta})

def candidato_list(request):
    candidatos = Candidato.objects.all()
    return render(request, 'candidato/candidato_list.html', {'candidatos': candidatos})

def candidato_create(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidato:candidato_list')
    else:
        form = CandidatoForm()
    return render(request, 'candidato/candidato_form.html', {'form': form})

def candidato_edit(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    if request.method == 'POST':
        form = CandidatoForm(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            return redirect('candidato:candidato_list')
    else:
        form = CandidatoForm(instance=candidato)
    return render(request, 'candidato/candidato_form.html', {'form': form})

def candidato_delete(request, pk):
    candidato = get_object_or_404(Candidato, pk=pk)
    if request.method == 'POST':
        candidato.delete()
        return redirect('candidato:candidato_list')
    return render(request, 'candidato/candidato_confirm_delete.html', {'candidato': candidato})


def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidato:status_list')
    else:
        form = StatusForm()
    return render(request, 'candidato/status_form.html', {'form': form})

def status_list(request):
    status = StatusContato.objects.all()
    return render(request, 'candidato/status_list.html', {'status': status})

def status_edit(request, pk):
    status = get_object_or_404(StatusContato, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('candidato:status_list')
    else:
        form = StatusForm(instance=status)
    return render(request, 'candidato/status_form.html', {'form': form})

def status_delete(request, pk):
    status = get_object_or_404(StatusContato, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('candidato:status_list')
    return render(request, 'candidato/status_confirm_delete.html', {'status': status})