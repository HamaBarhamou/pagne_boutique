# catalog/context.py
from django.conf import settings


def business_info(request):
    return {
        "BUSINESS_NAME": getattr(settings, "BUSINESS_NAME", "Boutique de Pagne"),
        "BUSINESS_TAGLINE": getattr(
            settings, "BUSINESS_TAGLINE", "Pagne de qualité à Niamey"
        ),
        "BUSINESS_PHONE": getattr(settings, "BUSINESS_PHONE", "+227 96 53 66 60"),
        "BUSINESS_WHATSAPP": getattr(
            settings, "BUSINESS_WHATSAPP", "22796536660"
        ),  # format international sans +
        "BUSINESS_ADDRESS": getattr(
            settings, "BUSINESS_ADDRESS", "Marché de Niamey, Niger"
        ),
        "BUSINESS_HOURS": getattr(settings, "BUSINESS_HOURS", "Lun–Sam : 8h–19h"),
        "BUSINESS_FACEBOOK": getattr(settings, "BUSINESS_FACEBOOK", ""),
        "BUSINESS_INSTAGRAM": getattr(settings, "BUSINESS_INSTAGRAM", ""),
    }
