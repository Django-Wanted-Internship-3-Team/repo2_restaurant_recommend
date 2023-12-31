# Generated by Django 4.2.6 on 2023-11-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 0), ('rating__lte', 5)), name='rating_0_to_5_constraint'),
        ),
    ]
