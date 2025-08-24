from django.shortcuts import render, get_object_or_404
from urllib.parse import quote
from django.conf import settings
from .models import Category, Product


def _wa_link(text: str):
    phone = getattr(settings, "BUSINESS_WHATSAPP", "")
    return f"https://wa.me/{phone}?text={quote(text)}" if phone else None


def home(request):
    categories = Category.objects.all()[:8]
    products = Product.objects.filter(is_active=True)[:16]
    hero_cta = _wa_link("Bonjour, je suis intéressé(e) par vos pagnes.")
    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "products": products,
            "hero_cta": hero_cta,
        },
    )


def product_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(
        request, "product_list.html", {"category": category, "products": products}
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    wa = _wa_link(f"Bonjour, je veux le pagne: {product.name} ({product.price} FCFA).")
    return render(request, "product_detail.html", {"product": product, "wa": wa})


def about(request):
    wa = _wa_link("Bonjour, je veux des informations sur votre boutique.")
    return render(request, "about.html", {"wa": wa})


def contact(request):
    wa = _wa_link("Bonjour, je veux commander un pagne.")
    maps_q = quote(getattr(settings, "BUSINESS_ADDRESS", "Niamey"))
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_q}"
    return render(request, "contact.html", {"wa": wa, "maps_url": maps_url})
