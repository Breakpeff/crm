from django.urls import path
from . import views

urlpatterns = [
    # Dashboard e Listagens
    path('dashboard/', views.dashboard, name='dashboard'),
    path('negocios/', views.lista_negocios, name='lista_negocios'),
    path('kanban/', views.kanban_negocios, name='kanban'),

    # Gestão de Leads (Oportunidades)
    path('novo-lead/', views.novo_lead, name='novo_lead'),
    path('editar-lead/<int:pk>/', views.editar_lead, name='editar_lead'),
    path('excluir-lead/<int:pk>/', views.excluir_lead, name='excluir_lead'),

    # Gestão de Clientes (Contatos e Empresas)
    path('contato/novo/', views.novo_contato, name='novo_contato'),
    path('empresa/nova/', views.nova_empresa, name='nova_empresa'),
    path('atualizar-status-lead/<int:pk>/', views.atualizar_status_lead, name='atualizar_status_lead'),
]