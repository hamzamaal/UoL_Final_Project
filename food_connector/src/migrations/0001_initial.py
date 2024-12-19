# Generated by Django 3.0.3 on 2024-12-15 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('street_number', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=10)),
                ('province', models.CharField(choices=[('Eastern Cape', 'Eastern Cape'), ('Free State', 'Free State'), ('Gauteng', 'Gauteng'), ('KwaZulu-Natal', 'KwaZulu-Natal'), ('Limpopo', 'Limpopo'), ('Mpumalanga', 'Mpumalanga'), ('North West', 'North West'), ('Northern Cape', 'Northern Cape'), ('Western Cape', 'Western Cape')], max_length=255)),
                ('country', models.CharField(default='South Africa', max_length=50)),
                ('organization_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]