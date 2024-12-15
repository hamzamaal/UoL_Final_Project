from django.shortcuts import render

# Example user view
def users(request):
    return render(request, 'users.html')

# path('', home, name='home'),  # Main page
# path('donations/', donations, name='donations'),  # Donation page
# path('users/', users, name='users'),  # User management page


