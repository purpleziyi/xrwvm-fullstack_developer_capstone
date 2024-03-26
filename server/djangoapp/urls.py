from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    # path(route="register", view=views.registration, name="register"),
    path('register/', TemplateView.as_view(template_name="index.html")),

    # path for login
    path(route='login', view=views.login_user, name='login'),
    
    # path for logout
    path(route='logout', view=views.logout_request, name="logout"),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
