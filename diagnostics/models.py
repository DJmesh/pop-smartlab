from django.db import models

class DiagnosticReport(models.Model):
    class Category(models.TextChoices):
        NORMAL = "normal", "Normal"
        CRITICA = "critica", "Crítica"

    title = models.CharField("Título", max_length=200)
    su_identifier = models.CharField("Identificador da SU", max_length=120, blank=True)
    user_name = models.CharField("Nome", max_length=120)
    user_email = models.EmailField("Email")
    message = models.TextField("Mensagem de diagnóstico")
    category = models.CharField("Categoria", max_length=20, choices=Category.choices, default=Category.NORMAL)

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
