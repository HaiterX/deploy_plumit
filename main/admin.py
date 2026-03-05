from django.contrib import admin
from django.utils.html import format_html

from .models import Case, CaseImage, CaseMobileBlock, CaseMobileBlockImage


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 1
    fields = ("image", "scale", "title", "subtitle", "sort")
    ordering = ("sort",)


class CaseMobileBlockInline(admin.StackedInline):
    model = CaseMobileBlock
    extra = 0
    show_change_link = True
    fields = ("layout", "order", "image", "title_gradient", "title_text", "text")


class CaseMobileBlockImageInline(admin.TabularInline):
    model = CaseMobileBlockImage
    extra = 0
    max_num = 4
    fields = ("image", "order")
    ordering = ("order",)


@admin.register(CaseMobileBlock)
class CaseMobileBlockAdmin(admin.ModelAdmin):
    inlines = [CaseMobileBlockImageInline]
    list_display = ("id", "case", "layout", "order")
    list_filter = ("layout",)
    ordering = ("case", "order", "id")


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    inlines = [CaseImageInline, CaseMobileBlockInline]
    list_display = ("title", "slug", "is_published", "sort", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "subtitle", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("created_at",)
    readonly_fields = ("cover_preview",)

    fieldsets = (
        ("Основное", {"fields": (
            "title", "slug", "subtitle", "description",
            "is_published", "sort",
            "show_on_home", "home_position",
            "show_on_works", "works_block", "works_position",
        )}),
        ("Картинки страницы", {"fields": (
            "cover_image", "cover_alt", "cover_scale", "cover_preview",
            "hero_image", "mockup_image", "sphera_bg_image", "contact_bg_image",
        )}),
        ("Тексты блоков", {"fields": ("task_text", "execution_text", "result_text")}),
        ("Desktop / Mobile", {"fields": (
            "desktop_text", "desktop_image",
            "desktop_title_gradient", "desktop_title_text",
        )}),
    )

    @admin.display(description="Превью обложки")
    def cover_preview(self, obj: Case):
        if not obj or not obj.cover_image:
            return ""
        scale = getattr(obj, "cover_scale", 100) or 100
        return format_html(
            '<img id="cover-preview-img" src="{}" style="width:{}%; max-width:100%; height:auto; border-radius:12px;" />',
            obj.cover_image.url,
            scale,
        )

    class Media:
        js = (
            "admin/js/case_cover_preview.js",
            "admin/js/clear_file_inputs.js",
        )