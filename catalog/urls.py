from django.urls import path
from django.contrib import admin
from . import views as catalog_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", catalog_views.home, name="home"),
    path("a-propos/", catalog_views.about, name="about"),
    path("contact/", catalog_views.contact, name="contact"),
    path("c/<slug:slug>/", catalog_views.product_list, name="product_list"),
    path("p/<slug:slug>/", catalog_views.product_detail, name="product_detail"),
]
