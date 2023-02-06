from django.urls import path


from django.conf.urls.static import static

from pateik_app.views import *
from pateik_core import settings

urlpatterns = [
    path("", main_page, name="main-page"),
    path("registration/", CreateUser.as_view(), name="register-page"),
    path("about/", AboutPage.as_view(), name="about-page"),
    path("payment/<int:pk>/", payment_view, name="payment"),
    path("ajax/load-cities/", load_times, name="ajax_load_times"),
    path("webhook/", stripe_webhook),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "pateik"
