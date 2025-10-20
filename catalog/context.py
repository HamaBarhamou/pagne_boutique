from .models import BusinessSetting


def business_context(request):
    s = BusinessSetting.get_solo()
    return {
        "BUSINESS_NAME": s.name,
        "BUSINESS_TAGLINE": s.tagline,
        "BUSINESS_ADDRESS": s.address,
        "BUSINESS_PHONE": s.phone,
        "BUSINESS_WHATSAPP": s.whatsapp,
        "BUSINESS_HOURS": s.hours,
        "BUSINESS_INSTAGRAM": s.instagram,
    }
