# Generated by Django 4.2.6 on 2024-01-20 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_alter_box_accounting_serial_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box_accounting',
            name='serial_num',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
