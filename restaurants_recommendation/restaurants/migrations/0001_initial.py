# Generated by Django 4.2.6 on 2023-11-01 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('do_si', models.CharField(help_text='도,시', max_length=32)),
                ('sgg', models.CharField(help_text='시,군,구', max_length=32)),
                ('longitude', models.CharField(max_length=32)),
                ('latitude', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'restaurant_locations',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_code', models.CharField(max_length=128, unique=True)),
                ('location_code', models.CharField(max_length=64, null=True)),
                ('business_name', models.CharField(max_length=64, null=True)),
                ('licensing_at', models.CharField(max_length=16, null=True)),
                ('operating_status', models.CharField(max_length=16, null=True)),
                ('closure_at', models.CharField(max_length=16, null=True)),
                ('floor_area', models.CharField(max_length=32, null=True)),
                ('water_supply_facility_type', models.CharField(max_length=32, null=True)),
                ('number_of_male_employees', models.IntegerField(null=True)),
                ('year', models.CharField(max_length=32, null=True)),
                ('multiple_use_facility', models.CharField(max_length=32, null=True)),
                ('grade_classification', models.CharField(max_length=32, null=True)),
                ('total_facility_size', models.CharField(max_length=32, null=True)),
                ('number_of_female_employees', models.IntegerField(null=True)),
                ('surrounding_area_description', models.CharField(max_length=32, null=True)),
                ('sanitary_business_type', models.CharField(max_length=32, null=True)),
                ('total_employees_count', models.IntegerField(null=True)),
                ('street_address', models.CharField(max_length=32, null=True)),
                ('parcel_address', models.CharField(max_length=32, null=True)),
                ('postal_code', models.CharField(max_length=32, null=True)),
                ('latitude', models.CharField(max_length=32)),
                ('longitude', models.CharField(max_length=32)),
                ('rating', models.FloatField(default=0.0)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurants.restaurantlocation')),
            ],
            options={
                'db_table': 'restaurants',
            },
        ),
    ]
