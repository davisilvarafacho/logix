from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# TODO colocar um warning que me fale quando eu não usei o self.get_queryset


class MultitenantManager(models.Manager):
    """
    Manager que filtra os registros pelo tenant do usuário logado.
    """

    def from_user(self, user):
        """
        Filtra os registros pelo tenant do usuário logado.
        """
        return self.get_queryset().filter(tenant=self.request.tenant)


class Base(models.Model):
    """
    Modelo base contendo campos padrão para controle interno do
    sistema, como data e hora de criação e alteração.
    """

    SIM_NAO = (
        ("S", "Sim"),
        ("N", "Não"),
    )

    ZERO_UM = (
        ("0", "0"),
        ("1", "1"),
    )

    ativo = models.BooleanField(
        _("ativo"),
        default=True,
        help_text="Se o registro está ativo ou não",
    )

    data_hora_criacao = models.DateTimeField(
        _("data e hora de criação"),
        auto_now_add=True,
        help_text="Data e hora da criação do registro",
    )

    data_hora_ultima_alteracao = models.DateTimeField(
        _("data e hora da última alteração"),
        auto_now=True,
        help_text="Data e hora da última alteração",
    )

    """
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("criador do registro"),
        on_delete=models.PROTECT,
        help_text="Usuário que criou o registro",
    )
    """

    objects = MultitenantManager()

    class Meta:
        abstract = True


zero_um = Base.ZERO_UM
sim_nao = Base.SIM_NAO


class Endereco(models.Model):
    ESTADOS = (
        ("RO", "Rondônia"),
        ("AC", "Acre"),
        ("AM", "Amazonas"),
        ("RR", "Roraima"),
        ("PA", "Pará"),
        ("AP", "Amapá"),
        ("TO", "Tocantins"),
        ("MA", "Maranhão"),
        ("PI", "Piauí"),
        ("CE", "Ceará"),
        ("RN", "Rio Grande do Norte"),
        ("PB", "Paraíba"),
        ("PE", "Pernambuco"),
        ("AL", "Alagoas"),
        ("SE", "Sergipe"),
        ("BA", "Bahia"),
        ("MG", "Minas Gerais"),
        ("ES", "Espírito Santo"),
        ("RJ", "Rio de Janeiro"),
        ("SP", "São Paulo"),
        ("PR", "Paraná"),
        ("SC", "Santa Catarina"),
        ("RS", "Rio Grande do Sul"),
        ("MS", "Mato Grosso do Sul"),
        ("MT", "Mato Grosso"),
        ("GO", "Goiás"),
        ("DF", "Distrito Federal"),
        ("EX", "Exterior"),
    )

    pais = models.CharField(_("País"), max_length=20, blank=True, default="Brasil")
    cep = models.CharField(_("Cep"), max_length=8)
    estado = models.CharField(_("Estado"), choices=ESTADOS, max_length=2)
    cidade = models.CharField(_("Cidade"), max_length=150)
    bairro = models.CharField(_("Bairro"), max_length=150)
    rua = models.CharField(_("Rua"), max_length=150)
    numero = models.CharField(_("Número"), max_length=8)
    complemento = models.CharField(
        _("Complemento"), max_length=100, blank=True, default=""
    )

    class Meta:
        abstract = True

estados = Endereco.ESTADOS
