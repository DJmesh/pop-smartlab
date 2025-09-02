from django.shortcuts import render

def index(request):
    tools = [
        {"icon": "🔌", "label": "Multímetro Digital"},
        {"icon": "🛠️", "label": "Jogo de Chaves"},
        {"icon": "🔧", "label": "Chaves Allen/Boca"},
        {"icon": "🤏", "label": "Pinça de Precisão"},
        {"icon": "🧤", "label": "Luvas Antiestática"},
        {"icon": "📸", "label": "Câmera Fotográfica"},
    ]
    return render(request, "pages/index.html", {"tools": tools})
