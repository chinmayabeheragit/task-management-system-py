# tasks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema

class TaskListView(APIView):
    @swagger_auto_schema(request_body=TaskSerializer)  # Shows fields for POST
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: TaskSerializer(many=True)})  # Shows fields for GET
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetailView(APIView):
    @swagger_auto_schema(responses={200: TaskSerializer})  # For GET
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=TaskSerializer)  # For PUT
    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={204: "No Content"})  # For DELETE
    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
