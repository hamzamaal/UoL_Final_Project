from django.urls import path
from src.views import views  # Ensure this is correctly imported


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),
    path('training/', views.training, name='training'),
    path('donors/', views.donors, name='donors'),
    # path('begin-donate/', views.begin_donate, name='begin-donate'),
    path('donor-register/', views.register_donor, name='donor-register'),
    path('donor-success/', views.donor_success, name='donor-success'),
    path('recipients/', views.recipients, name='recipients'),
    path('recipient-register/', views.recipient_register, name='recipient-register'),
    path('recipient-register/submit/', views.recipient_register_submit, name='recipient-register-submit'),
    path('get-started/', views.get_started, name='get-started'),  # Add this line
    path('liabilities/', views.liabilities, name='liabilities'),
    path('tax-benefits/', views.tax_benefits, name='tax-benefits'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]



