# Generated by Django 4.2.6 on 2023-10-14 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_id_equipment_box_equipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='box',
            name='ip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.boxip'),
        ),
    ]
