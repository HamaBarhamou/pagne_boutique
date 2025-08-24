from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalogue/<slug:slug>/", views.product_list, name="product_list"),
    path("produit/<slug:slug>/", views.product_detail, name="product_detail"),
    path("a-propos/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
