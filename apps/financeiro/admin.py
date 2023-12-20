import datetime

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as django_timezone

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from apps.financeiro.models import EntradaDinheiro, Despesa, Categoria, ItemListaDesejo


@admin.register(EntradaDinheiro)
class EntradaDinheiroAdmin(ModelAdmin):
    list_display = ("origem", "valor", "data_entrada")
    search_fields = ("origem",)
    ordering = ("-id",)
    list_filter = ("origem",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")


@admin.register(Despesa)
class DespesaAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = (
        "paga",
        "descricao",
        "valor_total",
        "entrada",
        "parcela",
        "total_parcelas",
        "categoria",
        "data_gasto",
    )

    fieldsets = (
        (None, {"fields": ("valor_total", "data_gasto", "descricao")}),
        (_("Classificações"), {"fields": ("categoria",)}),
        (
            _("Recorrência"),
            {
                "fields": (
                    "fixa",
                    "parcela",
                    "total_parcelas",
                )
            },
        ),
        (_("Informações de controle"), {"fields": ("paga", "entrada")}),
    )

    search_fields = ("descricao",)
    ordering = ("-fixa", "-id")
    list_filter = ("fixa", "categoria", "categoria__tipo", "entrada")
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")
    actions = ["duplicar_despesas_fixas", "gerar_parcelas_despesas_fixas"]

    @admin.action(description="Duplicar despesa(s)")
    def duplicar_despesas_fixas(modeladmin, request, queryset):
        for despesa in queryset:
            if not despesa.fixa:
                despesa.parcela += 1

            despesa.pk = None
            despesa.save()

    def get_5_dia_util(cls, data):
        count_dia_util = 0
        if data.weekday() > 6:
            count_dia_util += 1

        while count_dia_util < 4:
            data = data + datetime.timedelta(days=1)
            if data.weekday() < 6:
                count_dia_util += 1

        return data

    @admin.action(description="Gerar todas as parcelas")
    def gerar_parcelas_despesas_fixas(modeladmin, request, queryset):
        hoje = django_timezone.now()
        for despesa in queryset:
            if despesa.parcela < despesa.total_parcelas:
                for parcela in range(despesa.parcela + 1, despesa.total_parcelas + 1):
                    data_pagamento_parcela_futura = hoje + datetime.timedelta(
                        days=parcela * 30
                    )

                    data_pagamento_parcela_futura = (
                        data_pagamento_parcela_futura
                        - datetime.timedelta(days=data_pagamento_parcela_futura.day - 1)
                    )

                    quinto_dia_util = modeladmin.get_5_dia_util(
                        data_pagamento_parcela_futura
                    )

                    data_entrada_salario, _ = EntradaDinheiro.objects.get_or_create(
                        origem="SAL",
                        data_entrada__month=quinto_dia_util.month,
                        data_entrada__year=quinto_dia_util.year,
                        defaults={
                            "valor": 2500,
                            "data_entrada": data_pagamento_parcela_futura,
                        },
                    )

                    data_entrada_salario.data_entrada = quinto_dia_util
                    data_entrada_salario.save()

                    despesa.parcela += 1
                    despesa.pk = None
                    despesa.entrada = data_entrada_salario
                    despesa.save()


@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("nome", "tipo", "descricao",)
    search_fields = ("nome",)
    ordering = ("-id",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")


@admin.register(ItemListaDesejo)
class ItemListaDesejoAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("nome", "tipo", "valor", "comprado")
    list_filter = ("comprado", "tipo")
    search_fields = ("nome",)
    ordering = ("-id",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")
