from .models import BusinessSetting
from django.templatetags.static import static


def business_context(request):
    s = getattr(request, "store", None)
    return {
        "BUSINESS_NAME": s.name,
        "BUSINESS_TAGLINE": s.tagline,
        "BUSINESS_ADDRESS": s.address,
        "BUSINESS_PHONE": s.phone,
        "BUSINESS_WHATSAPP": s.whatsapp,
        "BUSINESS_HOURS": s.hours,
        "BUSINESS_INSTAGRAM": s.instagram,
        "BUSINESS_LOGO_URL": (
            s.logo.url if getattr(s, "logo", None) else static("img/logo.svg")
        ),
    }
