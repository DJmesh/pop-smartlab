from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os
import subprocess
import uuid


# -------------------------
# Modelo principal
# -------------------------
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


# -------------------------
# Helpers de upload
# -------------------------
MAX_VIDEO_MB = 20

def report_image_upload_to(instance, filename):
    # media/diagnostics/<report_id>/images/<uuid>.<ext>
    ext = os.path.splitext(filename)[1].lower() or ".jpg"
    return f"diagnostics/{instance.report_id}/images/{uuid.uuid4().hex}{ext}"

def report_video_upload_to(instance, filename):
    # media/diagnostics/<report_id>/videos/<uuid>.<ext>
    ext = os.path.splitext(filename)[1].lower() or ".mp4"
    return f"diagnostics/{instance.report_id}/videos/{uuid.uuid4().hex}{ext}"

def validate_video_size(file_obj):
    size_mb = file_obj.size / (1024 * 1024)
    if size_mb > MAX_VIDEO_MB:
        raise ValidationError(f"O vídeo excede {MAX_VIDEO_MB}MB (tamanho atual: {size_mb:.1f}MB).")


# -------------------------
# Anexos de Imagem
# -------------------------
class ImageAttachment(models.Model):
    report = models.ForeignKey(DiagnosticReport, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField("Imagem", upload_to=report_image_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Imagem #{self.pk} do Report {self.report_id}"

    def save(self, *args, **kwargs):
        """
        Comprime a imagem para WEBP, limita dimensões para economizar disco.
        """
        # Salva primeiro se for novo, para ter caminho (quando necessário)
        new = self.pk is None
        super_save = super().save
        if new:
            super_save(*args, **kwargs)

        # Se não tem arquivo válido, finalize
        if not self.file:
            return

        # Abre imagem
        try:
            self.file.seek(0)
            img = Image.open(self.file)
            img = img.convert("RGB")
        except Exception:
            # Não é imagem válida, não mexe
            if new:
                return
            return super_save(*args, **kwargs)

        # Redimensiona
        MAX_W, MAX_H = 1920, 1080
        img.thumbnail((MAX_W, MAX_H))

        # Salva em memória como WEBP
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=80, method=6)
        buf.seek(0)

        base, _ext = os.path.splitext(os.path.basename(self.file.name))
        new_name = f"{base}.webp"
        self.file.save(new_name, ContentFile(buf.read()), save=False)

        # Se não era novo, agora persistimos a troca do arquivo
        return super_save(update_fields=["file"] if not new else None)


# -------------------------
# Anexos de Vídeo
# -------------------------
class VideoAttachment(models.Model):
    report = models.ForeignKey(DiagnosticReport, on_delete=models.CASCADE, related_name="videos")
    file = models.FileField("Vídeo", upload_to=report_video_upload_to, validators=[validate_video_size])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Vídeo #{self.pk} do Report {self.report_id}"

    def save(self, *args, **kwargs):
        """
        Valida tamanho e tenta comprimir com ffmpeg (H.264 + AAC).
        """
        # Salva o upload primeiro
        new = self.pk is None
        super().save(*args, **kwargs)

        # Tenta comprimir
        try:
            in_path = self.file.path
            base, _ext = os.path.splitext(os.path.basename(in_path))
            out_dir = os.path.dirname(in_path)
            out_path = os.path.join(out_dir, f"{base}-cmp.mp4")

            cmd = [
                "ffmpeg", "-y",
                "-i", in_path,
                "-vcodec", "libx264", "-crf", "28", "-preset", "veryfast",
                "-acodec", "aac", "-b:a", "96k",
                out_path
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Substitui por comprimido
            with open(out_path, "rb") as f:
                self.file.save(os.path.basename(out_path), ContentFile(f.read()), save=False)

            super().save(update_fields=["file"])
            # Limpa original
            try:
                if os.path.exists(in_path):
                    os.remove(in_path)
            except Exception:
                pass

        except Exception:
            # ffmpeg indisponível/falhou -> mantém original
            pass
