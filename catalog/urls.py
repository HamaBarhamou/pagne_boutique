from django.urls import path
from django.contrib import admin
from . import views as catalog_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Site public
    path("", catalog_views.home, name="home"),
    path("a-propos/", catalog_views.about, name="about"),
    path("contact/", catalog_views.contact, name="contact"),
    path("c/<slug:slug>/", catalog_views.product_list, name="product_list"),
    path("p/<slug:slug>/", catalog_views.product_detail, name="product_detail"),
    # Staff area
    path(
        "staff/login/",
        auth_views.LoginView.as_view(template_name="staff/login.html"),
        name="login",
    ),
    path(
        "staff/logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"
    ),
    path("staff/", catalog_views.staff_dashboard, name="staff_dashboard"),
]
