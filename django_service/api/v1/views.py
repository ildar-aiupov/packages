import uuid

from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Package, PackageType
from .rabbit import rabbit_engine
from api.v1.serializers import (
    PackageCreateRequestSerializer,
    PackageCreateResponseSerializer,
    PackageListSerializer,
    PackageRetrieveSerializer,
    PackageTypesSerializer,
)


class PackageViewSet(viewsets.ModelViewSet):
    """Вьюсет посылок и типов посылок."""

    http_method_names = ["get", "post"]

    def get_queryset(self):
        """Формирует queryset для дальнейшей работы."""
        queryset = Package.objects.filter(sessionid=self.request.session.session_key)
        if self.action != "list":
            return queryset
        # делаем фильтр по параметру type, если задан
        if type := self.request.GET.get("type"):
            queryset = queryset.filter(type=type)
        return queryset

    def get_serializer_class(self):
        """Возвращает подходящий сериалайзер."""
        if self.request.method == "POST":
            return PackageCreateRequestSerializer
        if self.action == "list":
            return PackageListSerializer
        if self.action == "retrieve":
            return PackageRetrieveSerializer
        if self.action == "types":
            return PackageTypesSerializer

    @extend_schema(
        summary="Creates a new package", 
        description="Creates a new package",
        responses={
            201: PackageCreateResponseSerializer,
            500: None
        },
    )
    def create(self, request):
        """Создает новую посылку."""
        # задаем пользователю сессию, если отсутствует
        if not request.session.session_key:
            request.session.cycle_key()
        # формируем данные
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["uuid"] = str(uuid.uuid4())
        data["type"] = data["type"].name
        data["sessionid"] = request.session.session_key
        # отправляем данные в Rabbit. При неудаче возвращаем ошибку
        if rabbit_engine.send(data=data):
            return Response(
                {"uuid": data["uuid"]},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Returns a list of types of packages", 
        description="Returns a list of types of packages",
    )
    @method_decorator(cache_page(1))
    @method_decorator(vary_on_headers("Cookie"))
    @action(["get"], detail=False)
    def types(self, request):
        """Возвращает список типов посылок."""
        package_types = PackageType.objects.all()
        serializer = self.get_serializer(package_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Returns a list of packages", 
        description="Returns a paginated list of packages. You may customize your request with parameters",
        parameters=[
            OpenApiParameter(name='type', description='Filter by type of package', required=False, type=str),
        ],
    )
    @method_decorator(cache_page(1))
    @method_decorator(vary_on_headers("Cookie"))
    def list(self, *args, **kwargs):
        """Возвращает список посылок."""
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Returns data of specific package", 
        description="Returns data of specific package by its id",
    )
    @method_decorator(cache_page(1))
    @method_decorator(vary_on_headers("Cookie"))
    def retrieve(self, *args, **kwargs):
        """Возвращает данные по конкретной посылке."""
        return super().retrieve(*args, **kwargs)
