# Generated by Django 4.2.6 on 2023-12-30 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_alter_boxaccounting_serial_num_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='serial',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, unique=True),
        ),
    ]
