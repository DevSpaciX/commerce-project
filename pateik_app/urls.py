from django.urls import path


from django.conf.urls.static import static

from pateik_app.views import *
from pateik_core import settings

urlpatterns = [
    path("", main_page, name="main-page"),
    path("profile/", Profile.as_view(), name="profile"),
    path("logout/", logout_view, name="logout"),
    path("registration/", CreateUser.as_view(), name="register-page"),
    path("about/", AboutPage.as_view(), name="about-page"),
    path("payment/<int:pk>/", payment_view, name="payment"),
    path("payment-success/", payment_success, name="payment-success"),
    path("payment-denied/", payment_denied, name="payment-denied"),
    path("ajax/load-times/", load_times, name="ajax_load_times"),
    path("login/", login_view, name="login-page"),
    path("webhook/", stripe_webhook),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "pateik"
