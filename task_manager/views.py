from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task, Project
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrer les tâches des projets de l'utilisateur connecte
        return Task.objects.filter(project__created_by=self.request.user)

    def perform_create(self, serializer):
        # les validation supplémentaire lors de la création d'une tâche
        project = serializer.validated_data.get('project')

        # Vérifier que le projet appartient a l'utilisateurr
        if project.created_by != self.request.user:
            return Response(
                {"detail": "Vous ne pouvez créer des tâches que dans vos propres projets."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save()

    def perform_update(self, serializer):
        # Vérifier que seul le créateur du projet ou l'utilisateur assigné peut modifier
        task = self.get_object()

        if (task.project.created_by != self.request.user and
                task.assigned_to != self.request.user):
            return Response(
                {"detail": "Vous n'avez pas la permission de modifier cette tâche."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save()

    def perform_destroy(self, instance):
        # Vérifier que seul le créateur du projet peut supprimer une tâche
        if instance.project.created_by != self.request.user:
            return Response(
                {"detail": "Vous n'avez pas la permission de supprimer cette tâche."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):

        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):

        task = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {"detail": "Statut invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.status = new_status
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data)