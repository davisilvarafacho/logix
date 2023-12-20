from rest_framework import serializers
from .models import Despesa, EntradaDinheiro, Categoria


class DespesasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = "__all__"
        depth = 1


class EntradaDinheiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaDinheiro
        fields = "__all__"
        depth = 1


class MotivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
