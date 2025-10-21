from django.contrib import admin
from .models import Category, Product, BusinessSetting
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BusinessSetting)
class BusinessSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identité", {"fields": ("name", "tagline", "logo", "logo_preview")}),
        ("Coordonnées", {"fields": ("address", "phone", "whatsapp", "hours")}),
        ("Réseaux", {"fields": ("instagram",)}),
    )
    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="max-height:60px;border-radius:8px">', obj.logo.url
            )
        return "—"

    logo_preview.short_description = "Aperçu du logo"

    def has_add_permission(self, request):
        # Empêche d'ajouter plus d’une instance
        return not BusinessSetting.objects.exists()
