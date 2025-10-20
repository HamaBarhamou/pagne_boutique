from django.shortcuts import render, get_object_or_404
from urllib.parse import quote
from django.conf import settings
from .models import Category, Product
from django.core.paginator import Paginator


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
