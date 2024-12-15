from django.urls import path
# from views.donation_views import DonationView
from src.views.views import home
from src.views.donation_views import DonationView

from src.views.user_views import users

urlpatterns = [
    path('', home, name='home'),  # Main page
    path('donations/', DonationView, name='donations'),  # Donation page
    path('users/', users, name='users'),  # User management page
]


