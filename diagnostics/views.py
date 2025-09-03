from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils.timezone import make_aware
from datetime import datetime, time

from .models import DiagnosticReport, ImageAttachment, VideoAttachment
from .forms import DiagnosticReportForm, DiagnosticFilterForm, ImageUploadForm, VideoUploadForm


def create_report(request):
    if request.method == "POST":
        form = DiagnosticReportForm(request.POST)
        if form.is_valid():
            report = form.save()

            # Salva imagens, se houver
            for f in request.FILES.getlist("images"):
                ImageAttachment.objects.create(report=report, file=f)

            # Salva vídeos, se houver (valida tamanho via model validator)
            for f in request.FILES.getlist("videos"):
                va = VideoAttachment(report=report, file=f)
                va.full_clean()
                va.save()

            return redirect("diagnostics:detail", pk=report.pk)
    else:
        form = DiagnosticReportForm()

    return render(request, "diagnostics/form.html", {"form": form})


def report_detail(request, pk):
    report = get_object_or_404(DiagnosticReport, pk=pk)
    img_form = ImageUploadForm()
    vid_form = VideoUploadForm()

    if request.method == "POST":
        if "images" in request.FILES:
            img_form = ImageUploadForm(request.POST, request.FILES)
            if img_form.is_valid():
                for f in request.FILES.getlist("images"):
                    ImageAttachment.objects.create(report=report, file=f)
            return redirect("diagnostics:detail", pk=pk)

        if "videos" in request.FILES:
            vid_form = VideoUploadForm(request.POST, request.FILES)
            if vid_form.is_valid():
                for f in request.FILES.getlist("videos"):
                    va = VideoAttachment(report=report, file=f)
                    va.full_clean()
                    va.save()
            return redirect("diagnostics:detail", pk=pk)

    images = report.images.all()
    videos = report.videos.all()

    return render(request, "diagnostics/detail.html", {
        "report": report,
        "images": images,
        "videos": videos,
        "img_form": img_form,
        "vid_form": vid_form,
    })


def list_reports(request):
    qs = DiagnosticReport.objects.all()
    form = DiagnosticFilterForm(request.GET or None)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        category = form.cleaned_data.get("category")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        order_by = form.cleaned_data.get("order_by") or "-created_at"

        if q:
            qs = qs.filter(title__icontains=q)
        if category:
            qs = qs.filter(category=category)
        if start_date:
            start_dt = make_aware(datetime.combine(start_date, time.min))
            qs = qs.filter(created_at__gte=start_dt)
        if end_date:
            end_dt = make_aware(datetime.combine(end_date, time.max))
            qs = qs.filter(created_at__lte=end_dt)

        qs = qs.order_by(order_by)

    paginator = Paginator(qs, 10)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    return render(request, "diagnostics/list.html", {"form": form, "page_obj": page_obj})
