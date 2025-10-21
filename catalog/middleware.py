# catalog/middleware.py
from .models import BusinessSetting


class StoreResolverMiddleware:
    """
    Attache request.store en fonction du Host (domaine).
    Fallback: premier BusinessSetting actif.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = (request.get_host() or "").split(":")[0].lower()
        store = None
        if host:
            store = BusinessSetting.objects.filter(
                is_active=True, domain__iexact=host
            ).first()
        if not store:
            store = BusinessSetting.objects.filter(is_active=True).first()
        request.store = store
        return self.get_response(request)
