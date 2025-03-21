from rest_framework import serializers
from .models import Task, Project


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    assigned_to_username = serializers.ReadOnlyField(
        source='assigned_to.username',
        allow_null=True
    )
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'project',
            'project_name',
            'assigned_to',
            'assigned_to_username',
            'status',
            'deadline',
            'created_at',
            'is_overdue'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'project': {'required': True}
        }

    def get_is_overdue(self, obj):
        return obj.is_overdue()

    def validate_deadline(self, value):
        # Vérifier que la deadline n'est pas dans le passé
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("La date limite ne peut pas être dans le passé.")
        return value

    def validate(self, data):
        # Validation supplémentaire
        project = data.get('project')
        assigned_to = data.get('assigned_to')

        # Optionnel : Ajouter des règles de validation supplémentaires
        return data