from rest_framework import serializers

from .models import Package, PackageType


class PackageCreateRequestSerializer(serializers.ModelSerializer):
    """Сериалайзер входящих данных при регистрации посылки."""

    class Meta:
        model = Package
        fields = [
            "name",
            "weight",
            "type",
            "content_cost",
        ]


class PackageCreateResponseSerializer(serializers.Serializer):
    """Сериалайзер возвращаемого результата при успешной регистрации посылки."""

    uuid = serializers.CharField()


class PackageListSerializer(serializers.ModelSerializer):
    """Сериалайзер возвращаемого списка посылок."""

    class Meta:
        model = Package
        fields = [
            "uuid",
            "name",
            "weight",
            "type",
            "content_cost",
            "delivery_cost",
            "sessionid",
        ]


class PackageRetrieveSerializer(serializers.ModelSerializer):
    """Сериалайзер возвращаемых данных о конкретной посылке."""

    class Meta:
        model = Package
        fields = [
            "name",
            "weight",
            "type",
            "content_cost",
            "delivery_cost",
        ]


class PackageTypesSerializer(serializers.ModelSerializer):
    """Сериалайзер возвращаемого списка типов посылок."""

    class Meta:
        model = PackageType
        fields = [
            "id",
            "name",
        ]
