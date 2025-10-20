from django.contrib import admin
from .models import Category, Product, BusinessSetting


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
        ("Identité", {"fields": ("name", "tagline")}),
        ("Coordonnées", {"fields": ("address", "phone", "whatsapp", "hours")}),
        ("Réseaux", {"fields": ("instagram",)}),
    )

    def has_add_permission(self, request):
        # Empêche d'ajouter plus d'une instance
        return not BusinessSetting.objects.exists()
