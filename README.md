# POP — Padronização Organizacional de Procedimento (Smartlab)

Um projeto **Django 5** com front-end baseado em **Tailwind via CDN**, arquitetura de templates padronizada (partials de **navbar** e **footer**), e um app de negócio chamado **diagnostics** para registrar e consultar diagnósticos de **SUs (Smart Units)** no campus. Já vem pronto para **deploy no Render** (Blueprint `render.yaml`) e com **CI/CD via GitHub Actions** (dois modelos: Deploy Hook e API com espera).

> **Público-alvo:** este README foi pensado para você **e para um(a) estagiário(a)** que vai aprender o fluxo **do zero ao deploy**, incluindo decisões técnicas, bibliotecas, variações de ambiente (Windows/macOS/Linux), e um conjunto de **checklists e diagnósticos** de problemas comuns.

---

## 🔖 Índice

* [Visão Geral](#visão-geral)
* [Arquitetura do Projeto](#arquitetura-do-projeto)
* [Tecnologias & Bibliotecas](#tecnologias--bibliotecas)
* [Pré-requisitos](#pré-requisitos)
* [Clonando o Repositório](#clonando-o-repositório)
* [Configuração de Ambiente](#configuração-de-ambiente)

  * [Criando venv (Windows / Linux / macOS)](#criando-venv-windows--linux--macos)
  * [Instalando dependências](#instalando-dependências)
  * [Arquivo `.env` (local)](#arquivo-env-local)
  * [Variáveis de ambiente utilizadas](#variáveis-de-ambiente-utilizadas)
* [Configuração do Django](#configuração-do-django)

  * [Estrutura de pastas](#estrutura-de-pastas)
  * [Settings de produção e desenvolvimento](#settings-de-produção-e-desenvolvimento)
  * [Static files (WhiteNoise)](#static-files-whitenoise)
  * [Banco de dados (SQLite/Postgres)](#banco-de-dados-sqlitepostgres)
  * [Timezone e Localização](#timezone-e-localização)
* [Aplicativos do Projeto](#aplicativos-do-projeto)

  * [pages](#pages)
  * [diagnostics](#diagnostics)

    * [Modelo de dados](#modelo-de-dados)
    * [Forms](#forms)
    * [Views & URLs](#views--urls)
    * [Templates](#templates)
    * [Admin](#admin)
* [Executando localmente](#executando-localmente)

  * [Migrações e superusuário](#migrações-e-superusuário)
  * [Rodando o servidor de desenvolvimento](#rodando-o-servidor-de-desenvolvimento)
* [Testes (opcional)](#testes-opcional)
* [Padronização de Front-end](#padronização-de-front-end)

  * [Base, Navbar, Footer e Layout “sticky footer”](#base-navbar-footer-e-layout-sticky-footer)
  * [Index (POP) com explicação para leigos](#index-pop-com-explicação-para-leigos)
* [Deploy no Render (Blueprint)](#deploy-no-render-blueprint)

  * [Arquivo `render.yaml`](#arquivo-renderyaml)
  * [Como criar o serviço no Render](#como-criar-o-serviço-no-render)
  * [Variáveis no Render e segurança](#variáveis-no-render-e-segurança)
* [CI/CD com GitHub Actions](#cicd-com-github-actions)

  * [Workflow simples (Deploy Hook)](#workflow-simples-deploy-hook)
  * [Workflow com API e “wait”](#workflow-com-api-e-wait)
* [Guia de Ensino para Estagiários](#guia-de-ensino-para-estagiários)

  * [Roteiro sugerido de 90 minutos](#roteiro-sugerido-de-90-minutos)
  * [Checklist rápido de entendimento](#checklist-rápido-de-entendimento)
* [Troubleshooting (Erros Comuns)](#troubleshooting-erros-comuns)
* [Segurança & Boas Práticas](#segurança--boas-práticas)
* [Futuras Extensões](#futuras-extensões)
* [Apêndices](#apêndices)

  * [A. Comandos úteis do Django](#a-comandos-úteis-do-django)
  * [B. Fixtures de exemplo](#b-fixtures-de-exemplo)
  * [C. Convenções de commit](#c-convenções-de-commit)
  * [D. Diagrama de dados (ASCII)](#d-diagrama-de-dados-ascii)
  * [E. FAQ](#e-faq)

---

## Visão Geral

Este projeto implementa uma **POP (Padronização Organizacional de Procedimento)** aplicada ao **diagnóstico de sensores** e **SUs (Smart Units)** no Smartlab. A proposta é:

* Apresentar uma **página inicial** (POP para leigos), com objetivo, ferramentas e passos (stepper) — estilizada com Tailwind via CDN.
* Disponibilizar um **formulário de diagnóstico** para registrar ocorrências: título, identificador da SU, nome, e-mail, categoria (normal/crítica) e mensagem.
* Fornecer uma **página de busca** com filtros por título, categoria, intervalo de datas e ordenação.
* Entregar uma **arquitetura de templates** padronizada (base/partials) e um **layout sticky footer**.
* Estar pronto para **produção** no **Render** com `render.yaml`, **WhiteNoise** e **dj-database-url\`** para Postgres.
* Opcionalmente integrar **CI/CD** com GitHub Actions.

---

## Arquitetura do Projeto

* **Projeto Django**: `app`
* **Apps**:

  * `pages`: páginas de conteúdo (home/POP).
  * `diagnostics`: domínio de diagnósticos das SUs.
* **Templates**:

  * `templates/base.html` — layout comum (Tailwind CDN, fonte Inter, sticky footer).
  * `templates/partials/navbar.html` e `templates/partials/footer.html` — componentes reutilizáveis.
  * `templates/pages/index.html` — POP (com explicação para leigos).
  * `templates/diagnostics/form.html` e `templates/diagnostics/list.html` — CRUD simples (create + list/filter).
* **Static**:

  * `static/` — seus assets durante desenvolvimento (ex: `img/smartlogo-only.png`).
  * `staticfiles/` — destino do `collectstatic` em produção.

---

## Tecnologias & Bibliotecas

* **Django 5** — framework web (MTV) em Python.
* **Tailwind (via CDN)** — utilitários CSS rápidos sem build step.
* **WhiteNoise** — servir arquivos estáticos em produção sem servidor externo.
* **Gunicorn** — WSGI server para produção.
* **dj-database-url** — parse de `DATABASE_URL` (Postgres no Render).
* **psycopg2-binary** — driver Postgres.

`requirements.txt` mínimo:

```
Django>=5.0,<6.0
gunicorn
whitenoise
dj-database-url
psycopg2-binary
```

---

## Pré-requisitos

* **Python 3.12+** (recomendado) — verifique com `python --version`.
* **Git** — para clonar e versionar.
* (Opcional) **PostgreSQL** local — se quiser testar com banco real; caso contrário, SQLite já funciona.

---

## Clonando o Repositório

```bash
# via SSH
git clone git@github.com:SEU-USUARIO/SEU-REPO.git
# ou via HTTPS
# git clone https://github.com/SEU-USUARIO/SEU-REPO.git
cd SEU-REPO
```

---

## Configuração de Ambiente

### Criando venv (Windows / Linux / macOS)

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS (bash/zsh):**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Instalando dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Arquivo `.env` (local)

Crie um arquivo **`.env`** na raiz (para desenvolvimento):

```env
DJANGO_SECRET_KEY=django-insecure-8y$7H3rO8i0Gx0v#X9vH%1@f3$zJm6p!Rw^c2!bQe7KZpJfW4r
DJANGO_DEBUG=true
# DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/app_db
# RENDER_EXTERNAL_HOSTNAME=  # não usar localmente
```

> Em produção no Render, as variáveis virão do `render.yaml` e do painel do serviço.

### Variáveis de ambiente utilizadas

* `DJANGO_SECRET_KEY`: chave secreta do Django (produção deve **sempre** usar valor seguro).
* `DJANGO_DEBUG`: `true` (dev) / `false` (prod).
* `DATABASE_URL`: quando presente, `dj-database-url` usa este DSN (ex.: Postgres do Render). Se ausente, cai no SQLite local.
* `RENDER_EXTERNAL_HOSTNAME`: definida pelo Render; usada para `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

> Carregamento do `.env`: no dev você pode usar extensões do VSCode ou exportar variáveis manualmente. O projeto não depende de `python-dotenv`; se preferir, você pode instalar e adicionar o `load_dotenv()` em `manage.py`.

---

## Configuração do Django

### Estrutura de pastas

```
app/                    # projeto (settings/urls/wsgi)
├─ settings.py
├─ urls.py
├─ wsgi.py

pages/                  # app de conteúdo
  ├─ views.py
  ├─ urls.py
  └─ ...

diagnostics/            # app de negócio (diagnósticos)
  ├─ models.py
  ├─ forms.py
  ├─ views.py
  ├─ urls.py
  ├─ admin.py
  └─ ...

templates/
  ├─ base.html
  ├─ partials/
  │   ├─ navbar.html
  │   └─ footer.html
  ├─ pages/
  │   └─ index.html
  └─ diagnostics/
      ├─ form.html
      └─ list.html

static/
  └─ img/smartlogo-only.png

staticfiles/            # gerado pelo collectstatic em produção
```

### Settings de produção e desenvolvimento

O arquivo `app/settings.py` já está pronto para as duas situações:

* **Local (dev):** usa `.env`, `DJANGO_DEBUG=true`, banco **SQLite** por padrão, `STATICFILES_DIRS` aponta para `static/`.
* **Produção (Render):** Render define `RENDER_EXTERNAL_HOSTNAME`, e usamos `DATABASE_URL` do Postgres. `DEBUG=false`, WhiteNoise serve estáticos reunidos em `STATIC_ROOT=staticfiles/`.

Pontos-chave do `settings.py`:

* **WhiteNoise** no `MIDDLEWARE` logo após `SecurityMiddleware`.
* **STORAGES** com `CompressedManifestStaticFilesStorage`.
* **ALLOWED\_HOSTS** e **CSRF\_TRUSTED\_ORIGINS** populados a partir de `RENDER_EXTERNAL_HOSTNAME`.
* Banco via `dj_database_url.config(...)` fallback para SQLite.

### Static files (WhiteNoise)

* Durante o desenvolvimento, os assets vêm de `static/`.
* Em produção, o pipeline (`render.yaml`) executa:

  * `python manage.py collectstatic --noinput` → empacota para `staticfiles/`.
  * WhiteNoise serve esses arquivos com cache + manifest.

### Banco de dados (SQLite/Postgres)

* **Dev:** SQLite (simples e zero-config).
* **Prod:** Postgres (Render cria via `render.yaml`). O settings lê `DATABASE_URL` automaticamente.

### Timezone e Localização

* `LANGUAGE_CODE = "pt-br"`
* `TIME_ZONE = "America/Sao_Paulo"`
* `USE_TZ = True` (timestamps em UTC no banco; conversão feita pela aplicação).

---

## Aplicativos do Projeto

### pages

App simples de conteúdo. A view principal renderiza `templates/pages/index.html`, que contém a **explicação da POP** e a estrutura (Objetivo, Ferramentas, Processo). A navbar inclui links para `Novo Diagnóstico` e `Buscar`.

### diagnostics

Gerencia o cadastro e a busca de diagnósticos de SUs.

#### Modelo de dados

`diagnostics/models.py`:

```python
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
```

> Índices aceleram filtros por `category`, ordenações por `created_at` e buscas por `title`.

#### Forms

* `DiagnosticReportForm` (criação).
* `DiagnosticFilterForm` (filtros: título contém, categoria, data inicial/final, ordenação).

#### Views & URLs

* `create_report` (GET/POST) em `/diagnostics/new/`.
* `list_reports` (GET + filtros) em `/diagnostics/`.

Ambas definidas em `diagnostics/views.py` e registradas em `diagnostics/urls.py` (namespace `diagnostics`).

#### Templates

* `templates/diagnostics/form.html` — form com Tailwind.
* `templates/diagnostics/list.html` — filtros e paginação (10 itens/página), *badges* coloridas por categoria.

#### Admin

`diagnostics/admin.py` registra o modelo com `list_display`, `list_filter` e `search_fields` úteis.

---

## Executando localmente

### Migrações e superusuário

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Rodando o servidor de desenvolvimento

```bash
python manage.py runserver
```

* Home (POP): `http://127.0.0.1:8000/`
* Novo diagnóstico: `http://127.0.0.1:8000/diagnostics/new/`
* Buscar: `http://127.0.0.1:8000/diagnostics/`
* Admin: `http://127.0.0.1:8000/admin/`

---

## Testes (opcional)

O projeto não inclui testes de exemplo, mas recomendamos criar `tests/` por app (unitários para models/forms e de integração para views). Você pode iniciar com:

```bash
python manage.py test
```

---

## Padronização de Front-end

### Base, Navbar, Footer e Layout “sticky footer”

* `base.html` aplica `min-h-screen flex flex-col` no `<body>` e `flex-1` no `<main>`, garantindo que o footer tenha `mt-auto` e fique no fim em páginas com pouco conteúdo.
* `navbar.html` inclui links (Objetivo/Ferramentas/Processo/Novo Diagnóstico/Buscar) e usa o `static` para a logo.
* `footer.html` tem `mt-auto` e um container responsivo.

### Index (POP) com explicação para leigos

A página inicial foi reescrita para explicar **o que é POP** em linguagem simples (analogia com “receita”), além de listar ferramentas e passos, com botões para vídeos (placeholder) e rolagem suave.

---

## Deploy no Render (Blueprint)

### Arquivo `render.yaml`

Coloque na raiz do repositório:

```yaml
services:
  - type: web
    name: pop-smartlab
    env: python
    plan: free
    region: oregon
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate --noinput
    startCommand: gunicorn app.wsgi:application --log-file -
    envVars:
      - key: PYTHON_VERSION
        value: 3.12
      - key: DJANGO_DEBUG
        value: "false"
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: pop-db
          property: connectionString
    healthCheckPath: /

databases:
  - name: pop-db
    plan: free
```

### Como criar o serviço no Render

1. Conecte seu GitHub ao **Render**.
2. Vá em **New → Blueprint** e aponte para o seu repositório (que contém `render.yaml`).
3. O Render criará:

   * 1 **web service** (Python/Django)
   * 1 **Postgres** (DATABASE\_URL injetado)
4. O primeiro deploy roda `collectstatic` e `migrate` automaticamente.

> Em produção, `RENDER_EXTERNAL_HOSTNAME` é exportada pelo Render e o `settings.py` já lida com `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

### Variáveis no Render e segurança

* `DJANGO_SECRET_KEY` é **gerada automaticamente** no blueprint.
* `DJANGO_DEBUG` deve ser `false`.
* `DATABASE_URL` é preenchida a partir do Postgres criado no blueprint.
* Adicione outras vars conforme necessidade (por exemplo, provedores de e-mail/filas).

---

## CI/CD com GitHub Actions

Você pode acionar o deploy no Render após cada push na `main` via:

### Workflow simples (Deploy Hook)

1. No Render, habilite **Deploy Hook** do seu serviço e copie a URL.
2. No GitHub, em **Settings → Secrets and variables → Actions**, crie um secret:

   * `RENDER_DEPLOY_HOOK_URL` = URL copiada
3. Adicione `.github/workflows/deploy-render.yml`:

```yaml
name: CI & Deploy to Render

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - run: python manage.py check --deploy --fail-level WARNING

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Trigger Render deploy via Deploy Hook
        env:
          RENDER_DEPLOY_HOOK_URL: ${{ secrets.RENDER_DEPLOY_HOOK_URL }}
        run: |
          if [ -z "$RENDER_DEPLOY_HOOK_URL" ]; then echo "Missing hook"; exit 1; fi
          curl -fsS -X POST "$RENDER_DEPLOY_HOOK_URL"
```

### Workflow com API e “wait”

Se quiser que o pipeline **espere** o resultado do deploy:

* Secrets necessários no GitHub:

  * `RENDER_API_KEY` (Render → Settings → API Keys)
  * `RENDER_SERVICE_ID` (Service → Settings → Service ID)

```yaml
name: CI & Deploy to Render (API)

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - run: python manage.py check --deploy --fail-level WARNING

  deploy:
    needs: test
    runs-on: ubuntu-latest
    env:
      RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
      RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
    steps:
      - name: Trigger deploy
        id: trigger
        run: |
          set -e
          resp=$(curl -fsS -X POST \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            -H "Content-Type: application/json" \
            https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys \
            -d '{"clearCache":false}')
          echo "$resp"
          echo "deploy_id=$(echo "$resp" | jq -r '.id')" >> $GITHUB_OUTPUT

      - name: Wait for deploy
        run: |
          set -e
          dep_id="${{ steps.trigger.outputs.deploy_id }}"
          for i in {1..60}; do
            sleep 10
            resp=$(curl -fsS -H "Authorization: Bearer $RENDER_API_KEY" https://api.render.com/v1/deploys/$dep_id)
            status=$(echo "$resp" | jq -r '.status')
            echo "Status: $status"
            if [ "$status" = "live" ]; then exit 0; fi
            if [ "$status" = "failed" ] || [ "$status" = "canceled" ]; then echo "$resp"; exit 1; fi
          done
          echo "Timeout esperando deploy"; exit 1
```

---

## Guia de Ensino para Estagiários

### Roteiro sugerido de 90 minutos

1. **Panorama** (10 min): o que é POP e o objetivo do sistema.
2. **Arquitetura Django** (15 min): projeto `app`, apps `pages` e `diagnostics` (MTV).
3. **Templates e Tailwind** (10 min): base, partials, sticky footer.
4. **Modelagem** (10 min): `DiagnosticReport` + índices.
5. **Forms & Views** (10 min): criação e busca com filtros.
6. **Execução local** (10 min): venv, `.env`, migrações, runserver.
7. **Render** (15 min): blueprint `render.yaml`, variáveis, primeiro deploy.
8. **CI/CD** (10 min): GitHub Actions (hook ou API com wait).

### Checklist rápido de entendimento

* [ ] Entende a função do `settings.py` e variáveis de ambiente.
* [ ] Sabe onde ficam templates e como herdar `base.html`.
* [ ] Sabe criar/migrar modelos e registrar no admin.
* [ ] Consegue criar um diagnóstico e encontrá-lo com filtros.
* [ ] Roda localmente e sabe ler o log do servidor.
* [ ] Sabe acionar um deploy pelo Render e interpretar falhas do build.

---

## Troubleshooting (Erros Comuns)

* **`TemplateSyntaxError: Could not parse ... .split(',')`**:

  * Django template **não** executa métodos Python. Passe listas pelo **contexto** na view (como foi feito com `tools`).

* **`Invalid block tag 'static'` em partials**:

  * Carregue as tags com `{% load static %}` **no partial**, ou adicione `"builtins": ["django.templatetags.static"]` nos `TEMPLATES.OPTIONS` (já incluído neste projeto).

* **Footer “flutuando” no meio**:

  * Garanta `min-h-screen flex flex-col` no `<body>`, `flex-1` no `<main>` e `mt-auto` no `<footer>`.

* **Arquivos estáticos não carregam em produção**:

  * Verifique se `collectstatic` executou e se `STATIC_ROOT` existe.
  * Confirme `WhiteNoiseMiddleware` no `MIDDLEWARE` e `STORAGES` correto.

* **403 CSRF em produção**:

  * `RENDER_EXTERNAL_HOSTNAME` deve estar definido pelo Render. O settings adiciona em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

* **Erro de banco no Render**:

  * Confirme `DATABASE_URL` na aba de variáveis e se a DB existe (o blueprint cria `pop-db`).

---

## Segurança & Boas Práticas

* Nunca commit **SECRET\_KEY** de produção.
* Em produção, mantenha `DJANGO_DEBUG=false`.
* Habilite logs (já incluído no settings quando `DEBUG=False`).
* Faça backups regulares do Postgres (Render oferece opções na UI/API).
* Se adicionar autenticação, proteja rotas de escrita e dados sensíveis.

---

## Futuras Extensões

* **Autenticação** (login) para criar/editar/visualizar conforme perfil.
* **Upload de fotos** no diagnóstico (ex.: imagens do equipamento).
* **Exportação** (CSV/PDF) e **API REST** (Django REST Framework).
* **Notificações** por e-mail quando categoria = crítica.
* **Tags** ou **status** adicionais (em análise, resolvido, etc.).

---

## Apêndices

### A. Comandos úteis do Django

```bash
# checagens de produção
python manage.py check --deploy --fail-level WARNING

# criar nova app
python manage.py startapp nome_da_app

# migrações
python manage.py makemigrations
python manage.py migrate

# criar superusuário
python manage.py createsuperuser

# shell interativo
python manage.py shell
```

### B. Fixtures de exemplo

Salve como `diagnostics/fixtures/seed.json` e carregue com `python manage.py loaddata diagnostics/fixtures/seed.json`.

```json
[
  {
    "model": "diagnostics.diagnosticreport",
    "pk": 1,
    "fields": {
      "title": "Sensor de temperatura instável",
      "su_identifier": "SU-013",
      "user_name": "Maria Souza",
      "user_email": "maria@example.com",
      "message": "Oscilações na leitura após 10 min de operação.",
      "category": "normal",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    }
  },
  {
    "model": "diagnostics.diagnosticreport",
    "pk": 2,
    "fields": {
      "title": "Placa com odor de queimado",
      "su_identifier": "SU-021",
      "user_name": "João Lima",
      "user_email": "joao@example.com",
      "message": "Após ligar, apresenta aquecimento e odor.",
      "category": "critica",
      "created_at": "2025-01-05T09:30:00Z",
      "updated_at": "2025-01-05T09:30:00Z"
    }
  }
]
```

### C. Convenções de commit

* `feat:` nova funcionalidade
* `fix:` correção de bug
* `docs:` documentação
* `chore:` ajustes de build/infra
* `refactor:` refatoração sem mudar comportamento

### D. Diagrama de dados (ASCII)

```
+---------------------------+
| diagnostics_diagnosticreport |
+---------------------------+
| id (PK)                   |
| title (varchar 200)      |
| su_identifier (varchar)  |
| user_name (varchar)      |
| user_email (email)       |
| message (text)           |
| category (normal/critica)|
| created_at (datetime)    |
| updated_at (datetime)    |
+---------------------------+
Indexes: category, -created_at, title
```

### E. FAQ

**1) Preciso do Node/Tailwind CLI?**

> Não. Usamos Tailwind via CDN para simplificar. Se o projeto crescer, considere build com PostCSS ou Tailwind CLI para purgar classes e otimizar.

**2) Dá para usar Docker?**

> Sim, mas para manter o onboarding do estagiário simples, este repo usa Python venv + Render diretamente. Uma stack Docker pode ser adicionada futuramente.

**3) Como trocar o logo?**

> Substitua `static/img/smartlogo-only.png`. O `templates/partials/navbar.html` referencia via `{% static %}`.

**4) Como personalizar os textos da POP?**

> Edite `templates/pages/index.html`.

**5) Como paginar com mais/menos itens?**

> Ajuste `Paginator(qs, 10)` em `diagnostics/views.py`.

---

**FIM** — Se você (ou o estagiário) tiver dúvidas, use este README como mapa e compare seu ambiente com os checklists. O objetivo é que, ao final, a pessoa consiga **rodar localmente**, **entender a arquitetura**, **mandar para produção no Render** e **automatizar com CI/CD**.
