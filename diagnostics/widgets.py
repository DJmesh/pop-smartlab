from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    """
    Habilita seleção de múltiplos arquivos em um único campo.
    O ClearableFileInput padrão do Django não permite multiple=True.
    """
    allow_multiple_selected = True
