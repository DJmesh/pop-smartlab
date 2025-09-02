from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.timezone import make_aware
from datetime import datetime, time
from .models import DiagnosticReport
from .forms import DiagnosticReportForm, DiagnosticFilterForm

def create_report(request):
    if request.method == "POST":
        form = DiagnosticReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("diagnostics:list")
    else:
        form = DiagnosticReportForm()
    return render(request, "diagnostics/form.html", {"form": form})

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
