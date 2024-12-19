from django.db import models

class Donor(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(
        max_length=255,
        choices=[
            ('Eastern Cape', 'Eastern Cape'),
            ('Free State', 'Free State'),
            ('Gauteng', 'Gauteng'),
            ('KwaZulu-Natal', 'KwaZulu-Natal'),
            ('Limpopo', 'Limpopo'),
            ('Mpumalanga', 'Mpumalanga'),
            ('North West', 'North West'),
            ('Northern Cape', 'Northern Cape'),
            ('Western Cape', 'Western Cape'),
        ],
    )
    country = models.CharField(max_length=50, default='South Africa')
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Donors'  # Explicitly set table name
