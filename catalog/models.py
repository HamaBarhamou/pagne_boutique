from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    price = models.PositiveIntegerField(help_text="Prix en FCFA")
    thumbnail = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BusinessSetting(models.Model):
    name = models.CharField(
        "Nom de la boutique", max_length=120, default="ABH – Compagny"
    )
    tagline = models.CharField(
        "Slogan",
        max_length=160,
        blank=True,
        default="La sélection de pagnes qui font la différence",
    )
    address = models.CharField(
        "Adresse", max_length=200, blank=True, default="Niamey, Niger"
    )
    phone = models.CharField(
        "Téléphone", max_length=40, blank=True, default="+227 xx xx xx xx"
    )
    whatsapp = models.CharField(
        "WhatsApp (numéro au format international, ex: 227xxxxxxxx)",
        max_length=30,
        blank=True,
        default="",
    )
    hours = models.CharField(
        "Horaires", max_length=120, blank=True, default="Lun–Sam 9h–19h"
    )
    instagram = models.URLField("Lien Instagram", blank=True, default="")

    logo = models.ImageField(upload_to="branding/", blank=True, null=True)

    # Multi-site light
    domain = models.CharField(
        max_length=255,
        unique=True,
        help_text="Ex: boutique-amina.com ou amina.localhost",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Réglages boutique"
        verbose_name_plural = "Réglages boutique"

    def __str__(self):
        return f"{self.name} — {self.domain}"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj
