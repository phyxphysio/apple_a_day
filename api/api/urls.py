from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, re_path, include
from battery import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/user/", include("user.urls")),
    re_path(r"^api/energy-journal/$", views.energy_journal),
    re_path(r"^api/energy-journal/([0-9])$", views.energy_detail),
    path("api/recipe/", include("recipe.urls")),
]
