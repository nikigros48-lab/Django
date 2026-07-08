
from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskReadSerializer, TaskUpdateSerializer, TaskCreateSerializer
from ..models import Task


class TaskListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Task]:
        return Task.objects.select_related('details', 'category') \
            .prefetch_related('tags') \
            .filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskReadSerializer

    def get_serializer_context(self):
        serializer_context = dict(super().get_serializer_context())
        serializer_context['request'] = self.request
        return serializer_context

    def perform_create(self, serializer: TaskCreateSerializer):
        serializer.save(user=self.request.user)


class TaskAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskUpdateSerializer
        return TaskReadSerializer

    def get_serializer_context(self):
        context = dict(super().get_serializer_context())
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Task.objects.select_related('details', 'category') \
            .prefetch_related('tags') \
            .filter(user=self.request.user)