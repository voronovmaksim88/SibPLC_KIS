# Generated by Django 4.2.6 on 2024-01-08 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_box_accounting'),
    ]

    operations = [
        migrations.AddField(
            model_name='box_accounting',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.company'),
        ),
    ]
