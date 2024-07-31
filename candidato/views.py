from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidato, Meta
from .forms import CandidatoForm, MetaForm
import matplotlib.pyplot as plt
import io
import base64
from lideranca.models import Contato, Lideranca
from django.db.models import Count

def generate_contact_graph():
    # Get contact data
    contatos = Contato.objects.all()
    total_contatos = contatos.count()

    # If there are no contatos, return an empty image
    if total_contatos == 0:
        return "", total_contatos

    # Prepare data for the pie chart
    # Create a count for each Lideranca
    lideranca_counts = contatos.values('lideranca__nome').annotate(count=Count('lideranca'))
    labels = [l['lideranca__nome'] for l in lideranca_counts]
    sizes = [l['count'] for l in lideranca_counts]
    colors = plt.cm.Paired(range(len(labels)))

    # Generate a pie chart
    fig, ax = plt.subplots(figsize=(2, 2))  # Adjusted size to 30%
    wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=140)

    # Improve the readability of labels and percentages
    for text in texts:
        text.set_fontsize(8)  # Adjust font size for labels
    for autotext in autotexts:
        autotext.set_fontsize(8)  # Adjust font size for percentages

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add a legend
    legend_labels = [f"{label} ({size})" for label, size in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, title="Liderança", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')  # Adjust bbox_inches to fit the legend
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64, total_contatos

def index(request):
    contact_graph, total_contacts = generate_contact_graph()
    return render(request, 'principal.html', {
        'contact_graph': contact_graph,
        'total_contacts': total_contacts
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
