from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import TaskReadSerializer, TaskUpdateSerializer, TaskCreateSerializer
from ..models import Task


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request: Request) -> Response:
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)\
                            .select_related('details', 'category')\
                            .prefetch_related('tags')
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request: Request, task_id: int) -> Response:
    task = get_object_or_404(
        Task.objects.select_related('details', 'category')
                    .prefetch_related('tags'),
        id=task_id,
        user=request.user
    )

    if request.method == 'GET':
        serializer = TaskReadSerializer(task)
        return Response(serializer.data)

    elif request.method in ('PUT', 'PATCH'):
        serializer = TaskUpdateSerializer(
            task,
            data=request.data,
            partial=request.method == 'PATCH',   # для PUT все поля обязательны, для PATCH — нет
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)




# @api_view(['GET'])
# def get_tasks(request: Request) -> Response:
#     tasks = Task.objects.filter(user=request.user).select_related('details', 'category').prefetch_related('tags')
#     serializer = TaskReadSerializer(tasks, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def get_task(request: Request, task_id: int) -> Response:
#     task = get_object_or_404(Task.objects.select_related('details', 'category').prefetch_related('tags'), id=task_id, user=request.user)
#     serializer = TaskReadSerializer(task)
#     return Response(serializer.data)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_task(request: Request) -> Response:
#     serializer = TaskCreateSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid():
#         task = serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['PUT', 'PATCH'])
# @permission_classes([IsAuthenticated])
# def update_task(request: Request, task_id: int) -> Response:
#     task = get_object_or_404(Task, id=task_id, user=request.user)
#     serializer = TaskUpdateSerializer(task, data=request.data, partial=True, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_task(request: Request, task_id: int) -> Response:
#     task = get_object_or_404(Task, id=task_id, user=request.user)
#     task.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

