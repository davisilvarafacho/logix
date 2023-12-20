from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as django_timezone

from apps.system.base.models import Base


class EntradaDinheiro(Base):
    ORIGENS = (
        ("SAL", "Salário"),
        ("DEC", "Decimo terceiro"),
        ("FER", "Férias"),
        ("PRO", "Projeto"),
        ("MAN", "Manutenção"),
        ("OUT", "Outros"),
    )
    
    origem = models.CharField(
        _("tipo"),
        max_length=3,
        choices=ORIGENS,
        default="SAL",
    )

    valor = models.FloatField(
        _("valor"),
        help_text=_("Valor da entrada"),
        validators=[
            MinValueValidator(
                0.01, message=_("O valor da entrada deve ser maior que zero.")
            ),
        ],
    )

    data_entrada = models.DateField(
        _("data da entrada"),
        default=django_timezone.now,
    )

    def __str__(self):
        origem = None
        for valor_db, descricao in self.ORIGENS:
            if valor_db == self.origem:
                origem = descricao
                break

        return f'{origem} | {self.data_entrada.strftime("%m/%y")}'

    class Meta:
        db_table = "entrada_dinheiro"
        ordering = ["-id"]
        verbose_name = _("Entrada de dinheiro")
        verbose_name_plural = _("Entradas de dinheiro")


class Despesa(Base):
    entrada = models.ForeignKey(
        "EntradaDinheiro",
        verbose_name=_("entrada"),
        on_delete=models.CASCADE,
        related_name="saidas",
    )

    fixa = models.BooleanField(
        _("gasto fixo"),
        default=False,
        help_text=_("Informa se a despesa é fixa/recorrente ou não."),
    )

    parcela = models.PositiveIntegerField(
        _("parcela"),
        null=True,
        blank=True
    )

    total_parcelas = models.PositiveIntegerField(
        _("total de parcelas"),
        null=True,
        blank=True
    )

    valor_total = models.FloatField(
        _("valor"),
        help_text=_("Valor do pagamento"),
        validators=[
            MinValueValidator(
                0.01, message=_("O valor do pagamento deve ser maior que zero.")
            ),
        ],
    )

    descricao = models.TextField(_("descrição"))

    data_gasto = models.DateField(
        _("data do gasto"),
        default=django_timezone.now,
        help_text=_("Dia que foi gasto o dinheiro"),
    )

    categoria = models.ForeignKey(
        "Categoria",
        verbose_name=_("motivo"),
        on_delete=models.CASCADE,
        related_name="saidas",
    )

    paga = models.BooleanField(
        _("paga"),
        default=False,
        help_text=_("Informa se a despesa já foi paga ou não."),
    )

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "despesa"
        ordering = ["-id"]
        verbose_name = _("Despesa")
        verbose_name_plural = _("Despesas")


class Categoria(Base):
    TIPOS = (
        ("DES", "Despesas fixa"),  # Despesas fixas, como internet, faculdade, etc
        ("LAZ", "Lazer/Diversão"),  # Dinheiro gasto em rolês, coisas para mim, etc
        ("ECO", "Economizar"),  # Dinheiro guardado
        ("INV", "Investir"),  # Dinheiro investido
    )

    tipo = models.CharField(
        _("tipo"),
        max_length=3,
        choices=TIPOS,
        default="DES",
    )

    nome = models.CharField(_("nome"), max_length=50, help_text=_("Nome da categoria"))
    descricao = models.TextField(_("descrição"), blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "categoria"
        ordering = ["-id"]
        verbose_name = _("Categoria da despesa")
        verbose_name_plural = _("Categorias da despesa")


class ItemListaDesejo(Base):
    TIPOS = (
        ("LIV", "Livro"),
        ("SON", "Sonho/Objetivo"),
        ("ROP", "Roupa"),
        ("TEN", "Tênis"),
        ("PER", "Perfume"),
        ("OUT", "Outros"),
    )
    
    nome = models.CharField(_("nome"), max_length=50, help_text=_("Nome"))

    tipo = models.CharField(
        _("tipo"),
        max_length=3,
        choices=TIPOS,
        default="LIV",
    )

    valor = models.FloatField(
        _("valor"),
        help_text=_("Valor do desejo"),
        validators=[
            MinValueValidator(
                0.01, message=_("O valor do desejo deve ser maior que zero.")
            ),
        ],
    )

    link = models.URLField(_("link"), blank=True)

    comprado = models.BooleanField(
        _("comprado"),
        default=False,
    )

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "item_lista_desejo"
        ordering = ["-id"]
        verbose_name = _("Item da lista de desejos")
        verbose_name_plural = _("Lista de desejos")