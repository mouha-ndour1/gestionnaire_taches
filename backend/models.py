from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3, "Le nom du projet doit avoir au moins 3 caractères")]
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_manager_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
    ]

    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3, "Le titre doit avoir au moins 3 caractères")]
    )
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Vérifie si la tâche est en retard"""
        return self.status != 'done' and self.deadline < timezone.now().date()

    class Meta:
        ordering = ['-created_at']