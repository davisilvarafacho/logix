from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from apps.financeiro.models import (
    EntradaDinheiro,
    SaidaDinheiro,
    CategoriaGasto,
    ItemListaDesejo,
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
    list_display = (
        "descricao",
        "paga",
        "valor_total",
        "entrada",
        "obrigatoria",
        "parcela",
        "total_parcelas",
        "categoria",
        "data_gasto",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "valor_total",
                    "data_gasto",
                    "descricao",
                )
            },
        ),
        (_("Classificações"), {"fields": ("categoria",)}),
        (
            _("Recorrência"),
            {
                "fields": (
                    "parcela",
                    "total_parcelas",
                )
            },
        ),
        (
            _("Informações de controle"),
            {
                "fields": (
                    "paga",
                    "entrada",
                    "obrigatoria",
                )
            },
        ),
    )

    list_filter = (
        "categoria",
        "categoria__tipo",
        "entrada",
        "obrigatoria",
        "paga",
    )

    ordering = ("-id",)
    search_fields = ("descricao",)
    exclude = ("data_hora_criacao", "data_hora_atualizacao", "ativo")


@admin.register(CategoriaGasto)
class CategoriaAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = (
        "nome",
        "tipo",
        "descricao",
    )

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
