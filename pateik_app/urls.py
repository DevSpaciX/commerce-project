from django.urls import path


from django.conf.urls.static import static

from pateik_app.views import *
from pateik_core import settings

urlpatterns = [
    path("", main_page, name="main-page"),
    path("about/", AboutPage.as_view(), name="about-page"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "pateik"
