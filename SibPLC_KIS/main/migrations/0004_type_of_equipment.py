# Generated by Django 4.2.4 on 2023-09-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_country_countries_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type_of_equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
    ]
