# Generated by Django 4.2.20 on 2025-04-01 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_role_options_alter_shifttype_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifttype',
            name='break_minutes',
            field=models.PositiveIntegerField(default=0, verbose_name='休憩時間(分)'),
        ),
    ]
