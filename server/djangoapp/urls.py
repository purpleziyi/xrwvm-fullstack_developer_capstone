from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path(route="register", view=views.registration_request, name="register"),
    # path('register/', TemplateView.as_view(template_name="index.html")),   # off

    # path for login
    path(route="login", view=views.login_request, name="login"),
    # path('login/', TemplateView.as_view(template_name="index.html")),   # off
    
    # path for logout
    path(route='logout', view=views.logout_request, name="logout"),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='addreview/<int:dealer_id>/', view=views.add_review, name='add_review'),

    path(route='get_cars', view=views.get_cars, name ='getcars'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
