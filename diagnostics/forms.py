from django import forms
from .models import DiagnosticReport

class DiagnosticReportForm(forms.ModelForm):
    class Meta:
        model = DiagnosticReport
        fields = ["title", "su_identifier", "user_name", "user_email", "category", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
        }

class DiagnosticFilterForm(forms.Form):
    q = forms.CharField(label="Título contém", required=False)
    category = forms.ChoiceField(
        label="Categoria", required=False,
        choices=[("", "Todas")] + list(DiagnosticReport.Category.choices)
    )
    start_date = forms.DateField(label="De (data)", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(label="Até (data)", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    order_by = forms.ChoiceField(
        label="Ordenar por", required=False,
        choices=[
            ("-created_at", "Mais recente"),
            ("created_at", "Mais antigo"),
            ("title", "Título (A→Z)"),
            ("-title", "Título (Z→A)"),
        ],
        initial="-created_at",
    )
