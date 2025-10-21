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
        ("Domaine", {"fields": ("domain", "is_active")}),
        ("Coordonnées", {"fields": ("address", "phone", "whatsapp", "hours")}),
        ("Réseaux", {"fields": ("instagram",)}),
    )
    readonly_fields = ("logo_preview",)
    list_display = ("name", "domain", "is_active", "phone", "whatsapp")
    list_filter = ("is_active",)
    search_fields = ("name", "domain", "phone", "whatsapp")

    def logo_preview(self, obj):
        if obj and obj.logo:
            from django.utils.html import format_html

            return format_html(
                '<img src="{}" style="max-height:42px;border-radius:6px">', obj.logo.url
            )
        return "—"

    logo_preview.short_description = "Aperçu du logo"

    # on NE bloque plus l'add — on veut plusieurs boutiques à terme
    # def has_add_permission(self, request): return True
