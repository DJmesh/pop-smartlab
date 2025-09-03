from django.contrib import admin
from .models import DiagnosticReport, ImageAttachment, VideoAttachment

class ImageInline(admin.TabularInline):
    model = ImageAttachment
    extra = 0

class VideoInline(admin.TabularInline):
    model = VideoAttachment
    extra = 0

@admin.register(DiagnosticReport)
class DiagnosticReportAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "su_identifier", "user_name", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "su_identifier", "user_name", "user_email", "message")
    ordering = ("-created_at",)
    inlines = [ImageInline, VideoInline]

@admin.register(ImageAttachment)
class ImageAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "created_at")

@admin.register(VideoAttachment)
class VideoAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "created_at")
