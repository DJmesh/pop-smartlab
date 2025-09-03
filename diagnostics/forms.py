from django import forms
from django.core.exceptions import ValidationError
from .models import DiagnosticReport
from .widgets import MultiFileInput

MAX_VIDEO_MB = 200
MAX_VIDEO_BYTES = MAX_VIDEO_MB * 1024 * 1024


class DiagnosticReportForm(forms.ModelForm):
    class Meta:
        model = DiagnosticReport
        fields = ["title", "su_identifier", "user_name", "user_email", "message", "category"]
        labels = {
            "title": "Título",
            "su_identifier": "Identificador da SU",
            "user_name": "Nome",
            "user_email": "Email",
            "message": "Mensagem de diagnóstico",
            "category": "Categoria",
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
        }


class DiagnosticFilterForm(forms.Form):
    q = forms.CharField(label="Título contém", required=False)
    category = forms.ChoiceField(
        label="Categoria",
        required=False,
        choices=[("", "Todas")] + list(DiagnosticReport.Category.choices),
    )
    start_date = forms.DateField(
        label="De (data)", required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateField(
        label="Até (data)", required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    order_by = forms.ChoiceField(
        label="Ordenar por",
        required=False,
        choices=[
            ("-created_at", "Mais recentes"),
            ("created_at", "Mais antigos"),
            ("title", "Título A→Z"),
            ("-title", "Título Z→A"),
        ],
        initial="-created_at",
    )


class ImageUploadForm(forms.Form):
    images = forms.ImageField(
        label="Imagens",
        required=False,
        widget=MultiFileInput(attrs={
            "multiple": True,
            "accept": "image/*",
        }),
        help_text="Você pode selecionar múltiplas imagens (JPG, PNG, WEBP).",
    )


class VideoUploadForm(forms.Form):
    videos = forms.FileField(
        label="Vídeos (≤ 20 MB cada)",
        required=False,
        widget=MultiFileInput(attrs={
            "multiple": True,
            "accept": "video/*",
        }),
        help_text=f"Tamanho máximo por arquivo: {MAX_VIDEO_MB} MB.",
    )

    def clean_videos(self):
        """
        Valida cada arquivo:
        - tamanho ≤ 20 MB
        - (checagem leve) content_type começa com 'video/'
        """
        files = self.files.getlist("videos")
        for f in files:
            if f.size > MAX_VIDEO_BYTES:
                raise ValidationError(
                    f"O arquivo '{f.name}' excede {MAX_VIDEO_MB} MB (atual: {f.size / (1024*1024):.1f} MB)."
                )
            ctype = (getattr(f, "content_type", "") or "").lower()
            if ctype and not ctype.startswith("video/"):
                raise ValidationError(f"O arquivo '{f.name}' não parece ser um vídeo válido.")
        return files
