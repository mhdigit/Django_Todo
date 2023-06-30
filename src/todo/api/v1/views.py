from rest_framework.response import Response
from todo.models import Task
from .serializers import TaskSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class TodoListView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(user=self.request.user)
        )
    
    def list(self, request):
       
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    