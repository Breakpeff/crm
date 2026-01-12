import json # Importação necessária para o Kanban
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import JsonResponse # Necessário para o Kanban
from .models import Oportunidade, Empresa, Contato
from .forms import OportunidadeForm, ContatoForm
from django.db.models.functions import TruncDay
from django.db.models import Count
from datetime import datetime, timedelta    
# --- DASHBOARD & LISTAGEM ---
@login_required
def dashboard(request):
    # Pega todos os negócios do usuário logado
    meus_negocios = Oportunidade.objects.filter(vendedor=request.user)
    
    # Se aparecer apenas 1 e você tem 2, verifique se o 'vendedor' do segundo 
    # é realmente o usuário logado no banco de dados.
    
    vendas_ganhas_queryset = meus_negocios.filter(estagio__iexact='ganho')
    vendas_mes = vendas_ganhas_queryset.count()
    
    soma_total = meus_negocios.aggregate(Sum('valor'))['valor__sum'] or 0
    leads_recentes = meus_negocios.order_by('-id')[:5]
    valor_formatado = f"{soma_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # --- DADOS PARA OS GRÁFICOS ---
    
    # 1. Gráfico de Linha (Vendas Ganhas)
    # Filtramos apenas as que possuem data e status ganho
    vendas_por_dia = (
        vendas_ganhas_queryset
        .annotate(dia=TruncDay('data_criacao')) # Verifique se o nome é data_criacao
        .values('dia')
        .annotate(total=Sum('valor'))
        .order_by('dia')
    )
    
    labels_vendas = [v['dia'].strftime('%d/%m') for v in vendas_por_dia]
    dados_vendas = [float(v['total']) for v in vendas_por_dia]

    # 2. Gráfico de Pizza (Status conforme seu print)
    # Vamos contar cada estágio presente no seu pipeline
    status_counts = meus_negocios.values('estagio').annotate(total=Count('id'))
    
    # Criamos um dicionário para mapear os nomes que aparecem na sua imagem
    mapping = {
        'GANHO': 0,
        'PERDIDO': 0,
        'NOVO': 0,
        'QUALIFICADO': 0,
        'EM PROGRESSO': 0
    }
    
    for s in status_counts:
        status_nome = s['estagio'].upper() # Converte para maiúsculo para bater com o print
        if status_nome in mapping:
            mapping[status_nome] = s['total']

    dados_status = list(mapping.values())
    labels_status = list(mapping.keys())

    context = {
        'nome_vendedor': request.user.username,
        'vendas_mes': vendas_mes,
        'valor_total': valor_formatado,
        'leads': leads_recentes,
        'labels_vendas': labels_vendas,
        'dados_vendas': dados_vendas,
        'labels_status': labels_status, # Passando os nomes dinâmicos
        'dados_status': dados_status,
    }
    return render(request, 'crm/dashboard.html', context)
@login_required
def lista_negocios(request):
    negocios = Oportunidade.objects.filter(vendedor=request.user).order_by('-id')

    search_query = request.GET.get('search')
    if search_query:
        negocios = negocios.filter(
            Q(contato__nome__icontains=search_query) | 
            Q(contato__empresa__nome__icontains=search_query)
        )

    filtro = request.GET.get('filtro')
    titulo = "Todos os Negócios"
    if filtro:
        negocios = negocios.filter(estagio=filtro)
        titulo = f"Negócios: {filtro.replace('_', ' ').capitalize()}"

    return render(request, 'crm/lista_negocios.html', {
        'objetos': negocios, 
        'titulo_pagina': titulo,
        'search_query': search_query
    })

# --- VISÃO KANBAN ---

@login_required
def kanban_negocios(request):
    negocios = Oportunidade.objects.filter(vendedor=request.user)
    
    colunas = {
        'novo': negocios.filter(estagio='novo'),
        'qualificado': negocios.filter(estagio='qualificado'),
        'em_progresso': negocios.filter(estagio='Negociação'),
        'ganho': negocios.filter(estagio='ganho'),
        'perdido': negocios.filter(estagio='perdido'),
    }
    
    return render(request, 'crm/kanban.html', {'colunas': colunas})

@login_required
def atualizar_status_lead(request, pk):
    """View que salva a nova posição do lead ao arrastar no Kanban"""
    if request.method == 'POST':
        data = json.loads(request.body)
        lead = get_object_or_404(Oportunidade, pk=pk, vendedor=request.user)
        lead.estagio = data.get('estagio')
        lead.save()
        return JsonResponse({'status': 'sucesso'})

# --- FLUXO DE CADASTRO (CLIENTES) ---

@login_required
def nova_empresa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            Empresa.objects.create(nome=nome)
            return redirect('novo_contato')
    return render(request, 'crm/nova_empresa.html')

@login_required
def novo_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ContatoForm()
    return render(request, 'crm/novo_contato.html', {'form': form})

# --- GESTÃO DE LEADS (OPORTUNIDADES) ---

@login_required
def novo_lead(request):
    if request.method == "POST":
        form = OportunidadeForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.vendedor = request.user
            lead.save()
            return redirect('dashboard')
    else:
        form = OportunidadeForm()
    return render(request, 'crm/novo_lead.html', {'form': form})

@login_required
def editar_lead(request, pk):
    lead = get_object_or_404(Oportunidade, pk=pk, vendedor=request.user)
    if request.method == "POST":
        form = OportunidadeForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OportunidadeForm(instance=lead)
    return render(request, 'crm/editar_lead.html', {'form': form, 'lead': lead})

@login_required
def excluir_lead(request, pk):
    lead = get_object_or_404(Oportunidade, pk=pk, vendedor=request.user)
    if request.method == "POST":
        lead.delete()
        return redirect('dashboard')
    return render(request, 'crm/excluir_confirmar.html', {'lead': lead})

@login_required
def atualizar_status_lead(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lead = get_object_or_404(Oportunidade, pk=pk, vendedor=request.user)
            lead.estagio = data.get('estagio')
            lead.save()
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'metodo_nao_permitido'}, status=405)