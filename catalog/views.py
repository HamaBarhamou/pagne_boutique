from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from urllib.parse import quote
from django.conf import settings
from .models import Category, Product
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm


def _is_staff(user):
    return user.is_active and user.is_staff


@user_passes_test(_is_staff)
def staff_products_list(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.select_related("category").all().order_by("-id")
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(slug__icontains=q) | Q(category__name__icontains=q)
        )

    paginator = Paginator(qs, 15)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "staff/products/list.html", {"page_obj": page_obj, "q": q})


@user_passes_test(_is_staff)
def staff_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Produit créé avec succès.")
            return redirect("staff_products_list")
    else:
        form = ProductForm()
    return render(request, "staff/products/form.html", {"form": form, "mode": "create"})


@user_passes_test(_is_staff)
def staff_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit mis à jour.")
            return redirect("staff_products_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "staff/products/form.html",
        {"form": form, "mode": "edit", "product": product},
    )


@user_passes_test(_is_staff)
def staff_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produit supprimé.")
        return redirect("staff_products_list")
    return render(request, "staff/products/confirm_delete.html", {"product": product})


@user_passes_test(_is_staff)
def staff_product_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = not product.is_active
    product.save(update_fields=["is_active"])
    messages.info(request, f"Produit {'activé' if product.is_active else 'désactivé'}.")
    return redirect("staff_products_list")


@user_passes_test(_is_staff)
def staff_dashboard(request):
    # Stats simples pour démarrer
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    categories = Category.objects.annotate(n=Count("products")).order_by("-n")[:10]

    return render(
        request,
        "staff/dashboard.html",
        {
            "total_products": total_products,
            "active_products": active_products,
            "categories": categories,
        },
    )


def _wa_link(text: str):
    phone = getattr(settings, "BUSINESS_WHATSAPP", "") or ""
    return f"https://wa.me/{phone}?text={quote(text)}" if phone else None


def home(request):
    categories = Category.objects.all()[:8]
    products = Product.objects.filter(is_active=True).order_by("-id")[:16]
    hero_cta = _wa_link("Bonjour, je suis intéressé(e) par vos pagnes.")
    return render(
        request,
        "home.html",
        {"categories": categories, "products": products, "hero_cta": hero_cta},
    )


def product_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = category.products.filter(is_active=True)

    q = request.GET.get("q", "").strip()
    order = request.GET.get("order", "")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(slug__icontains=q))
    if order == "new":
        qs = qs.order_by("-id")
    elif order == "price_asc":
        qs = qs.order_by("price")
    elif order == "price_desc":
        qs = qs.order_by("-price")
    else:
        qs = qs.order_by("name")

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/product_list.html",
        {
            "current_category": category,
            "page_obj": page_obj,
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    wa = _wa_link(f"Bonjour, je veux le pagne: {product.name} ({product.price} FCFA).")
    # proposer 4 produits de la même catégorie (si possible)
    related = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)
        .order_by("-id")[:4]
    )
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "wa": wa, "related_products": related},
    )


def about(request):
    wa = _wa_link("Bonjour, je veux des informations sur votre boutique.")
    return render(request, "about.html", {"wa": wa})


def contact(request):
    wa = _wa_link("Bonjour, je veux commander un pagne.")
    maps_q = quote(getattr(settings, "BUSINESS_ADDRESS", "Niamey"))
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_q}"
    return render(request, "contact.html", {"wa": wa, "maps_url": maps_url})
