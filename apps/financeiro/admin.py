from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from apps.financeiro.models import (
    EntradaDinheiro,
    SaidaDinheiro,
    MotivoGasto,
    ItemListaDesejo,
    DestinoGasto,
)


@admin.register(EntradaDinheiro)
class EntradaDinheiroAdmin(ModelAdmin):
    list_display = ("origem", "valor", "data_entrada")
    search_fields = ("origem",)
    ordering = ("-id",)
    list_filter = ("origem",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")


@admin.register(SaidaDinheiro)
class SaidaDinheiroAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_per_page = 15

    list_display = (
        "descricao",
        "classe",
        "valor_total",
        "paga",
        "parcela",
        "total_parcelas",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "descricao",
                    "valor_total",
                    "paga",
                )
            },
        ),
        (
            _("Pagamento"),
            {
                "fields": (
                    "entrada",
                    "destino",
                    "data_gasto",
                )
            },
        ),
        (
            _("Recorrência"),
            {
                "fields": (
                    "parcela",
                    "total_parcelas",
                    "despesa",
                )
            },
        ),
        (
            _("Gerenciamento e controle"),
            {
                "fields": (
                    "classe",
                )
            },
        ),
        (
            _("Informações Complementares"),
            {
                "fields": (
                    "parcial",
                    "saida"
                )
            },
        ),
    )

    list_filter = ("paga", "entrada", "classe")
    ordering = ("-id",)
    search_fields = ("descricao",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")

    actions = (
        "calcular_total_gastos",
        "marcar_como_paga",
        "marcar_como_nao_paga",
        "duplicar_saida",
    )

    @admin.action(description=_("Marcar como paga"))
    def marcar_como_paga(cls, request, queryset):
        for saida in queryset:
            saida.paga = True
            saida.save()

    @admin.action(description=_("Marcar como não paga"))
    def marcar_como_nao_paga(cls, request, queryset):
        for saida in queryset:
            saida.paga = False
            saida.save()

    @admin.action(description=_("Duplicar saída"))
    def duplicar_saida(cls, request, queryset):
        for saida in queryset:
            saida.pk = None
            saida.paga = False

            if saida.parcela and saida.parcela < saida.total_parcelas:
                saida.parcela += 1

            saida.save()

    @admin.action(description=_("Calcular total dos gastos"))
    def calcular_total_gastos(cls, request, queryset):
        valor_total_gastos = queryset.aggregate(valor_total_gastos=Sum("valor_total"))[
            "valor_total_gastos"
        ]
        valor_total_gastos = round(valor_total_gastos, 2) if valor_total_gastos else 0
        valor_total_gastos = str(valor_total_gastos).replace(".", ",")

        messages.add_message(
            request, messages.INFO, f"O total de gastos é: R$ {valor_total_gastos}"
        )


@admin.register(MotivoGasto)
class MotivoGastoAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("nome",)
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


@admin.register(DestinoGasto)
class DestinoGastoAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("nome",)
    search_fields = ("nome",)
    ordering = ("-id",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")
