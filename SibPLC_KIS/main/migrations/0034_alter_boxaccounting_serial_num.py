# Generated by Django 4.2.4 on 2023-12-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_remove_boxaccounting_project_boxaccounting_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxaccounting',
            name='serial_num',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
    ]
